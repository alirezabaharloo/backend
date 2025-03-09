from django.shortcuts import render
from rest_framework.generics import *
from rest_framework import status
from rest_framework.response import Response
from ..serializers import *
from ..permissions import *
from rest_framework.permissions import IsAuthenticated
from utilities import send_resset_password_mail
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import SellerUserProfile


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        """
            Return ProfileSerializer if user.is_seller is False otherwise Return SellerProfileSerializer
        """

        serializer_class = SellerProfileSerializer  if isinstance(self.get_object(), SellerUserProfile) else ProfileSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
        


    def get_object(self):
        user = self.request.user
        # if /profile/{email} use (important for admins to see all profiles)
        if (email:=self.kwargs.get("email")):
            if user.is_superuser:
                user_obj = get_object_or_404(User, email=email)
                return user_obj.get_profile_obj()
            
            else:
                raise ValidationError({'permission_error': 'forbidden user!'})
        

        # else return SellerUserProfile if our user is seller otherwise return  UserProfile
        return user.get_profile_obj()
        

class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class SellerListView(ListAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = SellerListSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = SellerUserProfile.objects.all()
    filterset_fields = ['status']



class ProductListVIew(ListAPIView):
    pass


class ProductDetaliView(RetrieveAPIView):
    pass



class ShopView(GenericAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsSellerUserWithPerm]

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            shop = srz_data.save()
            data = {
                'message': 'shop successfully created!',
                'seller': request.user,
                'shop': shop.name 
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    