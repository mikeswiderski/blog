from django.test import TestCase, Client
from django.urls import reverse
from apps.posts.models import Post
from apps.users.models import User


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.U = 'testuser'
        self.P = 'testpassword'
        self.user = User.objects.create_user(username=self.U, password=self.P)
        self.post_create_url = reverse('post-create')
        self.post = {
            'title': 'Testtitle', 
            'body': 'TestBody',      
        }
        return super().setUp() 

class PostCreationTest(BaseTest):

    def test_can_create_post(self):
        self.assertEqual(Post.objects.count(), 0)
        self.client.login(username=self.U, password=self.P)
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        self.assertEqual(Post.objects.count(), 1)

    def test_create_redirects_after_form_success(self):
        self.client.force_login
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_authorid_equals_userid(self):
        self.client.login(username=self.U, password=self.P)
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        obj = Post.objects.all().first()
        self.assertEqual(obj.author.id, self.user.id)

    def test_invalid_entry_create(self):
        self.client.login(username=self.U, password=self.P)
        post_data = {
            'title': 'Testtitle',    
        }
        response = self.client.post(self.post_create_url, post_data, format='text/html')
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "body", "This field is required.")

    def test_login_required(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.U, password=self.P)
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)


class PostDetailTest(BaseTest):

    def test_detail_view_post_doesnt_exists(self):
        response = self.client.get(reverse('post-detail', kwargs={'post_id': 4}))
        self.assertEqual(response.status_code, 404)  

    def test_detail_view(self):

        self.client.login(username=self.U, password=self.P)
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        obj = Post.objects.all().first()
        response = self.client.get(reverse('post-detail', kwargs={'post_id': obj.id}))
        self.assertEqual(response.status_code, 200)  