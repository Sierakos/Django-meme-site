from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

# Create your tests here.

class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Crete only user. Profile is creating instantly when account is created.
        """
        user = User.objects.create_user(username='testuser', email='testuser@email.com', password='Abecadlo1')

    def test_user_and_profile_exist(self):
        """
        Test user and profile is connected properly
        """
        profile = Profile.objects.get(id=1)
        user = profile.user
        self.assertEqual(user.username, 'testuser')


    def test_default_profile_image(self):
        """
        Test user have default path to profile pic
        """
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.image.url, '/media/profile_pics/default.jpg')

    