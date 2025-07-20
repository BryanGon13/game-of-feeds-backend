from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profile

class ProfileDetailViewTests(APITestCase):
    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.adam_profile = Profile.objects.get(owner=self.adam)

    def test_can_retrieve_profile_with_valid_id(self):
        response = self.client.get(f'/profiles/{self.adam_profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_update_own_profile(self):
        self.client.login(username='adam', password='pass')
        url = f'/profiles/{self.adam_profile.id}/'
        data = {'bio': 'Updated bio'}
        response = self.client.patch(url, data, format='json')  # PATCH instead of PUT
        self.adam_profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.adam_profile.bio, 'Updated bio')   

    def test_user_cannot_update_other_profile(self):
        bryan = User.objects.create_user(username='bryan', password='pass')
        self.client.login(username='bryan', password='pass')
        url = f'/profiles/{self.adam_profile.id}/'
        data = {'bio': 'Hacked bio!'}
        response = self.client.put(url, data)
        self.adam_profile.refresh_from_db()
        self.assertNotEqual(self.adam_profile.bio, 'Hacked bio!')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfileListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')
        User.objects.create_user(username='bryan', password='pass')

    def test_can_list_profiles(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)