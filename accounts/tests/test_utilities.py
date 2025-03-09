from django.test import TestCase
from utilities import permission_detector

class PermissionDetectorTests(TestCase):

    def test_one_perm(self):
        response = permission_detector(admin=True, seller=False)
        self.assertEqual(response, 'admin')

    def test_to_many_perms(self):
        response = permission_detector(admin=True, seller=True)
        self.assertEqual(response, 'admin,seller')

    def test_normal_user_perm(self):
        response = permission_detector(admin=False,seller=False)
        self.assertEqual(response, 'normal')