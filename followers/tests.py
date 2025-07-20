from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Follower

# Create your tests here.

class FollowerTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='jon', password='pass')
        self.user2 = User.objects.create_user(username='arya', password='pass')

    def test_logged_in_user_can_follow_another_user(self):
        self.client.login(username='jon', password='pass')
        response = self.client.post('/followers/', {'followed': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follower.objects.count(), 1)
        self.assertEqual(Follower.objects.get().owner, self.user1)

    def test_logged_out_user_cannot_follow(self):
        response = self.client.post('/followers/', {'followed': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_unfollow(self):
        self.client.login(username='jon', password='pass')
        follow = Follower.objects.create(owner=self.user1, followed=self.user2)
        response = self.client.delete(f'/followers/{follow.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follower.objects.count(), 0)

    def test_user_cannot_unfollow_others_relationship(self):
        follow = Follower.objects.create(owner=self.user1, followed=self.user2)
        self.client.login(username='arya', password='pass')
        response = self.client.delete(f'/followers/{follow.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Follower.objects.count(), 1)