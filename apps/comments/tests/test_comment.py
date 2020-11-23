from django.test import TestCase, Client
from django.urls import reverse
from apps.posts.models import Post
from apps.users.models import User
from apps.comments.models import Comment

class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post_create_url = reverse('post-create')
        self.comment = {
            'body': "comment test body",
        } 
        self.post = {
            'title': 'Testtitle', 
            'body': 'TestBody',      
        }
        return super().setUp() 

class CommentCreationTest(BaseTest):

    def test_can_create_comment(self):
        self.assertEqual(Post.objects.count(), 0)
        self.client.login(username=self.username, password=self.password)
        self.client.post(self.post_create_url, self.post, format='text/html')
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        obj = Post.objects.all().first()
        response = self.client.post(reverse('comment-create', kwargs={'post_id': obj.id}), self.comment, format='text/html')
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.all().first()
        self.assertEqual(comment.post.id , obj.id)
        self.assertEqual(comment.author.id, self.user.id)
