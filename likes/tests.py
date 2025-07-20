from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post
from .models import Like

# Create your tests here.

class LikeListViewTests(APITestCase):
    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.post = Post.objects.create(owner=self.adam, caption='Test caption')

    def test_user_can_create_like(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_logged_out_user_cannot_like(self):
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LikeDetailViewTests(APITestCase):
    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.bryan = User.objects.create_user(username='bryan', password='pass')
        self.post = Post.objects.create(owner=self.adam, caption='Test caption')
        self.like = Like.objects.create(owner=self.adam, post=self.post)

    def test_user_can_delete_own_like(self):
        self.client.login(username='adam', password='pass')
        response = self.client.delete(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_others_like(self):
        self.client.login(username='bryan', password='pass')
        response = self.client.delete(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)