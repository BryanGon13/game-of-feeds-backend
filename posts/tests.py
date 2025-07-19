from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework import APITestCase

# Create your tests here.

class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')
    
    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, caption='a caption')
        response = self.client.get ('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

