from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from ..models import User, SellerUserProfile
from ..views import ChangePasswordView, ResetPasswordCheckTokenView
from django.conf import settings
from datetime import datetime
from datetime import timedelta
from jwt import ExpiredSignatureError, InvalidTokenError, DecodeError
import jwt
from .utils import UserTokenMixin
from unittest import mock

class RegisterTests(APITestCase):


    def test_valid_data(self):
        self.client.post(
            "/register/",
            data={
               "email": "alireza@gmail.com",
                "password": "41148",
                "password1": "41148",
            }
        )
        self.assertEqual(User.objects.all().count(), 1)


    def test_invalid_data(self):
        response = self.client.post(
            "/register/",
            data={
               "email": "alireza@gmail.com",
                "password": "123",
                "password1": "41148",
            }
        )
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(response.status_code, 400)


    def test_user_exist_error(self):
        # creating user
        User.objects.create_user(email='alireza@gmail.com', password='1234')

        # post to register view with that user
        response = self.client.post(
            "/register/",
            data={
               "email": "alireza@gmail.com",
                "password": "123",
                "password1": "41148",
            }
        )
        self.assertEqual(response.status_code, 400)


    def test_register_seller_user(self):
        self.client.post(
            "/register/seller",
            data={
               "email": "abol@gmail.com",
                "password": "41148",
                "password1": "41148",
            }
        )
        user = User.objects.first()
        self.assertTrue(user.is_seller)
        self.assertEqual(SellerUserProfile.objects.all().count(), 1)



class ChangePasswordTetss(APITestCase): 

    def setUp(self):
        self.user = User.objects.create_user("alireza@gmail.com", "41148")
        self.factory = APIRequestFactory()

    def test_valid_data(self):
        request = self.factory.post("change_password/", data={
            'old_password': "41148",
            'password': '1234',
            'password1': '1234'
        })
        force_authenticate(request, self.user)

        response = ChangePasswordView.as_view()(request)

        self.assertEqual(response.status_code, 200)


    def test_invalid_old_password(self):
        request = self.factory.post("change_password/", data={
            'old_password': "1234",
            'password': '41148',
            'password1': '41148'
        })
        force_authenticate(request, self.user)

        response = ChangePasswordView.as_view()(request)

        self.assertEqual(response.status_code, 400)


    def test_invalid_same_password(self):
        request = self.factory.post("change_password/", data={
            'old_password': "41148",
            'password': '123',
            'password1': '1234'
        })
        force_authenticate(request, self.user)

        response = ChangePasswordView.as_view()(request)

        self.assertEqual(response.status_code, 400)



class ResetPasswordTests(APITestCase):


    def setUp(self):
        """
            create test user and change http self.client header with that user access token
        """
        self.user = User.objects.create_user(email='abol@gmail.com', password='41148')
        self.token = self.client.post('/login/', data={'email': "abol@gmail.com", 'password': "41148"}).data.get("access")

        # assign Authorization | Bearer {token} to the http header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_check_valid_token(self):
        now = datetime.now()
        payload = {
            'increment_version': 0,
            'user_id':self.user.id,
            'iat': now,
            'exp': now + timedelta(hours=2),
        }
        token = jwt.encode(key=settings.SECRET_KEY, payload=payload, algorithm="HS256")

        response = self.client.post(f'/reset_password/check/{token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.data['user_id']), self.user.id)
    

    def test_expire_token(self):
        now = datetime.now()
        payload = {
            'increment_version': 0,
            'user_id':self.user.id,
            'iat': now,
            'exp': now - timedelta(minutes=30), # assume the token have expired 30 minutes ago
        }
        token = jwt.encode(key=settings.SECRET_KEY, payload=payload, algorithm="HS256")

        resposne = self.client.post(f'/reset_password/check/{token}')

        self.assertEqual(resposne.status_code, 400)
        self.assertEqual(resposne.data['message'], "token is expired!")


    def test_invalid_token(self):
        now = datetime.now()
        payload = {
            'increment_version': 0,
            'user_id':self.user.id,
            'iat': now,
            'exp': now + timedelta(minutes=30),
        }
        token = jwt.encode(key=settings.SECRET_KEY, payload=payload, algorithm="HS256")
        token=token.replace(token[len(token) - 1], 'E') # invalidate token with change the last index of that

        resposne = self.client.post(f'/reset_password/check/{token}')

        self.assertEqual(resposne.status_code, 400)
        self.assertEqual(resposne.data['message'], "Invalid token.")


    
    def test_increment_version_error(self):
        now = datetime.now()
        payload = {
            'increment_version': 0,
            'user_id':self.user.id,
            'iat': now,
            'exp': now + timedelta(hours=2),
        }
        token = jwt.encode(key=settings.SECRET_KEY, payload=payload, algorithm="HS256")
        resposne = self.client.post(f'/reset_password/check/{token}')
        self.assertEqual(resposne.status_code, 200)
        
        # reuse that token for checking increment error
        resposne = self.client.post(f'/reset_password/check/{token}')
        self.assertEqual(resposne.status_code, 400)
        self.assertEqual(resposne.data['message'], 'token is invalid (increment version error!).')




class ProfileViewTests(UserTokenMixin, APITestCase):
    
    def test_anonoumos_user_GET(self):
        client = APIClient()
        response = client.post('/profile/')

        self.assertEqual(response.status_code, 401)


    def test_normal_user_GET(self):
        # assign Authorization | Bearer {token} to the http header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_user_token}")
        response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.keys(), {'first_name', 'last_name', 'phone_number', 'image'})


    def test_seller_user_GET(self):
        # assign Authorization | Bearer {token} to the http header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_user_token}")
        response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.keys(), {'first_name', 'last_name', 'phone_number', 'national_code', 'image'})


    def test_admin_pannel_for_access_to_any_user_profile(self):
        # assign Authorization | Bearer {token} to the http header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_user_token}")
        response = self.client.get("/profile/seller@gmail.com")

        self.assertEqual(response.status_code, 200)
        

    def test_admin_pannel_gey_any_profile_with_forbbiden_user(self):
        # assign Authorization | Bearer {token} to the http header
        # we can use each seller, normal or anonymous and the output will be the same!
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_user_token}") 
        response = self.client.get("/profile/seller@gmail.com") 

        self.assertEqual(response.status_code, 400)


class CreateShopTests(UserTokenMixin, APITestCase):
    def test_anonymous_user(self):
        response = self.client.post('/shop/', data={'name': 'aligSHop', 'cell_phone': '57523825'})

        self.assertEqual(response.status_code, 401)


    def test_forbidden_user(self):
        # assign Authorization | Bearer {token} to the http header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_user_token}")

        response = self.client.post('/shop/', data={'name': 'aligSHop', 'cell_phone': '57523825'})

        self.assertEqual(response.status_code, 403)


    def test_seller_with_status_false(self):
        # assign Authorization | Bearer {token} to the http header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_user_token}")
        
        response = self.client.post('/shop/', data={'name': 'aligSHop', 'cell_phone': '57523825'})
        self.assertEqual(response.status_code, 403)


    # def test_seller_with_status_True(self):
    #     # creating new seller user with status True
    #     seller_user: User = User.objects.create_selleruser(email='seller_status_true@gmail.com', password='41148')
    #     seller_user.seller_profile.status = True
    #     seller_user.save()

    #     print(seller_user.is_seller)
    #     print(seller_user.seller_profile.status)

    #     # obtain user token
    #     seller_user_token = self.client.post('/login/', data={'email': 'seller_status_true@gmail.com', 'password': '41148'}).data.get("access")

    #     print(seller_user_token)

    #     # assign Authorization | Bearer {token} to the http header
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {seller_user_token}")
        
    #     response = self.client.post('/shop/', data={'name': 'aligSHop', 'cell_phone': '57523825'})


    #     self.assertEqual(response.status_code, 200)