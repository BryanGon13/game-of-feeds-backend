from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post
from comments.models import Comment

class CommentListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='arya', password='pass')
        self.post = Post.objects.create(owner=self.user, caption='Valar Morghulis')

    def test_can_list_comments(self):
        Comment.objects.create(owner=self.user, post=self.post, content='Nice post!')
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='arya', password='pass')
        response = self.client.post('/comments/', {'post': self.post.id, 'content': 'Amazing!'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_logged_out_user_cannot_create_comment(self):
        response = self.client.post('/comments/', {'post': self.post.id, 'content': 'I should not post'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        self.arya = User.objects.create_user(username='arya', password='pass')
        self.sansa = User.objects.create_user(username='sansa', password='pass')
        self.post = Post.objects.create(owner=self.arya, caption='Winter is coming')
        self.comment = Comment.objects.create(owner=self.arya, post=self.post, content='Watch out!')

    def test_can_retrieve_comment_with_valid_id(self):
        response = self.client.get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_update_own_comment(self):
        self.client.login(username='arya', password='pass')
        response = self.client.put(f'/comments/{self.comment.id}/', {'content': 'Changed!'})
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment.content, 'Changed!')

    def test_user_cannot_update_others_comment(self):
        self.client.login(username='sansa', password='pass')
        response = self.client.put(f'/comments/{self.comment.id}/', {'content': 'Nope!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_own_comment(self):
        self.client.login(username='arya', password='pass')
        response = self.client.delete(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_user_cannot_delete_others_comment(self):
        self.client.login(username='sansa', password='pass')
        response = self.client.delete(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)