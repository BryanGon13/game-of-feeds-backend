from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase

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

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'caption': 'a caption'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post('/posts/', {'caption': 'a caption'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.bryan = User.objects.create_user(username='bryan', password='pass')

        self.post1 = Post.objects.create(
            owner=self.adam, caption='test caption'
        )
        self.post2 = Post.objects.create(
            owner=self.bryan, caption='test another caption'
        )
        
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get(f'/posts/{self.post1.id}/')
        self.assertEqual(response.data['caption'], 'test caption')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'caption': 'test a new caption'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.caption, 'test a new caption')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_post_they_dont_own(self):
        self.client.login(username='bryan', password='pass')
        response = self.client.put('/posts/1/', {'caption': 'test a new caption'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    


    