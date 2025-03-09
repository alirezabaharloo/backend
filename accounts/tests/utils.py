from ..models import User, USER_TYPES


class UserTokenMixin:
    ADDITIONAL_PROPERTIES = {
        'normal': {},
        'seller': {},
        'admin': {}
    }

    def setUp(self):
        """ 
            create test user and change http self.client header with that user access token
        """
        User.objects.create_user(email='normal@gmail.com', password='41148', **self.ADDITIONAL_PROPERTIES['normal'])
        User.objects.create_selleruser(email='seller@gmail.com', password='41148', **self.ADDITIONAL_PROPERTIES['seller'])
        User.objects.create_superuser(email='admin@gmail.com', password='41148', **self.ADDITIONAL_PROPERTIES['admin'])

        # store access token per user 
        self.normal_user_token = self.client.post('/login/', data={'email': "normal@gmail.com", 'password': "41148"}).data.get("access")
        self.seller_user_token = self.client.post('/login/', data={'email': 'seller@gmail.com', 'password': '41148'}).data.get("access")
        self.super_user_token = self.client.post('/login/', data={'email': 'admin@gmail.com', 'password': '41148'}).data.get("access")


