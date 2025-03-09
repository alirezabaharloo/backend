from django.test import TestCase
from ..models import User, UserProfile, SellerUserProfile


class UserModelTest(TestCase):


    def test_profile_should_create_after_user_created_NormalUserProfile(self):
        User.objects.create_user('alireza@gmail.com', '41148')
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserProfile.objects.all().count(), 1)


    def test_profile_should_create_after_user_created_SellerUserProfile(self):
        User.objects.create_selleruser('alireza@gmail.com', '41148')
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(SellerUserProfile.objects.all().count(), 1)