from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from ..serializers import *
from rest_framework.permissions import IsAuthenticated
import jwt
from datetime import datetime, timedelta
from utilities import send_resset_password_mail
from rest_framework.views import APIView
from jwt import ExpiredSignatureError, InvalidTokenError, DecodeError
from django.shortcuts import get_object_or_404
from ..permissions import IsSuperUser

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, seller=None):
        srz_data = self.serializer_class(data=request.data, context={'seller': seller})
        if srz_data.is_valid():
            user = srz_data.save()

            data ={
                'message': 'user seccessfully registerd!',
                'email': user.email
            }
            return Response(data, status=status.HTTP_200_OK)
        
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterSellerView(RegisterView):
    
    def post(self, request):
        return super().post(request, seller=True)



class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        srz_data = self.serializer_class(data=request.data, context={'user': request.user})
        if srz_data.is_valid():
            srz_data.save()

            data = {
                'message': 'your password change successfully!'
            }

            return Response(data, status=status.HTTP_200_OK)
        
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ResetPasswordSendTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        now = datetime.now()
        payload = {
            'user_id':request.user.id,
            'iat': now,
            'exp': now + timedelta(hours=2),
            'increment_version': request.user.increment_version,
        }
        token = jwt.encode(key=settings.SECRET_KEY, payload=payload, algorithm="HS256")

        print(f"http://localhost:8000/reset_password/check/{token}")

        # send_reset_password_mail(request.user.email, token)

        data = {
            'message': 'email have sent to you!',
            'email': request.user.email
        }

        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordCheckTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, token):

        try:  
            # decode token
            paylod = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]) 
            if paylod['increment_version'] == request.user.increment_version:

                # increase increment version to prevent using the token reuse
                user = request.user
                user.increment_version += 1
                user.save()

                return Response({
                    'message': 'token is valid!',
                    'user_id': paylod['user_id'],
                }, status=status.HTTP_200_OK)
            
            else:
                message='token is invalid (increment version error!).'

        except ExpiredSignatureError:  
            message = "token is expired!"

        except InvalidTokenError:  
            message = "Invalid token."

        except DecodeError:  
            message ="Error during decoding the token."  

        except Exception as e:  
            message=f"An unexpected error occurred: {str(e)}"
        
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        
        

class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()

            data = {
                'message': 'your password successfully changed!'
            }

            return Response(data, status=status.HTTP_200_OK)
        
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class EnableSellerStatusView(APIView):
    # permission_classes = [IsSuperUser]

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get("email"))
        user.seller_profile.status = True
        user.seller_profile.save()

        data = {
            'message': 'seller successfully authenticated!',
            'email': user.email
        }

        return Response(data, status=status.HTTP_200_OK)