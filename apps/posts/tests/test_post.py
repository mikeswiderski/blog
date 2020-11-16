from django.test import TestCase, Client
from django.urls import reverse
from apps.posts.models import Post
from apps.users.models import User
from apps.tags.models import Tag


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post_create_url = reverse('post-create')
        self.post = {
            'title': 'Testtitle', 
            'body': 'TestBody', 
            'tags': 'test1,test2,test3',     
            'status': 'DRAFT',
        }
        self.post2 = {
            'title': 'Testtitle2', 
            'body': 'TestBody2', 
            'status': 'PUBLISHED', 
        }
        return super().setUp() 
        

class PostCreationTest(BaseTest):

    def test_can_create_post(self):
        self.assertEqual(Post.objects.count(), 0)
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        self.assertEqual(Post.objects.count(), 1)
        
    def test_create_redirects_after_form_success(self):
        self.client.force_login
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_authorid_equals_userid(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        obj = Post.objects.all().first()
        self.assertEqual(obj.author.id, self.user.id)

    def test_can_create_tags(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        obj = Post.objects.all().first()
        self.assertEqual(obj.tags.count(), 3)

    def test_invalid_tag_entry_create(self):
        self.client.login(username=self.username, password=self.password)
        post_data = {
            'title': 'Testtitle',
            'body': 'TestBody',
            'tags': 'test1,test2,test3%',    
        }
        response = self.client.post(self.post_create_url, post_data, format='text/html')
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "tags", 'Letters, digits, space, dash only.')

    def test_invalid_entry_create(self):
        self.client.login(username=self.username, password=self.password)
        post_data = {
            'title': 'Testtitle',    
        }
        response = self.client.post(self.post_create_url, post_data, format='text/html')
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "body", "This field is required.")

    def test_login_required(self):
        response = self.client.get(self.post_create_url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.post_create_url)
        self.assertEqual(response.status_code, 200)


class PostDetailTest(BaseTest):

    def test_detail_view_post_doesnt_exists(self):
        response = self.client.get(reverse('post-detail', kwargs={'post_id': 4}))
        self.assertEqual(response.status_code, 404)  

    def test_detail_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.post_create_url, self.post, format='text/html')
        obj = Post.objects.all().first()
        response = self.client.get(reverse('post-detail', kwargs={'post_id': obj.id}))
        self.assertEqual(response.status_code, 200)  


class PostUserListTest(BaseTest):

    def test_user_list(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post(self.post_create_url, self.post, format='text/html')
        response = self.client.get(reverse('post-user-list'))
        self.assertEqual(response.status_code, 200)  


class PostUpdateTest(BaseTest):

    def test_user_cant_update_someone_elses_post(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post(self.post_create_url, self.post, format='text/html')
        self.client.logout()
        self.assertEqual(Post.objects.count(), 1)
        obj = Post.objects.all().first() 
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.post(reverse('post-update', kwargs={'post_id': obj.id}), self.post2, format='text\html')  
        self.assertEqual(Post.objects.count(), 1)
        obj = Post.objects.all().first()
        self.assertEqual(obj.title, 'Testtitle')
        self.assertEqual(obj.status, 'DRAFT')
    
    def test_post_updates(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post(self.post_create_url, self.post, format='text/html')
        self.assertEqual(Post.objects.count(), 1)
        obj = Post.objects.all().first() 
        response = self.client.post(reverse('post-update', kwargs={'post_id': obj.id}), self.post2, format='text\html')
        self.assertEqual(Post.objects.count(), 1)
        obj = Post.objects.all().first()
        self.assertEqual(obj.title, 'Testtitle2')
        self.assertEqual(obj.status, 'PUBLISHED')

    def test_post_update_cant_change_published_to_draft(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post(self.post_create_url, self.post2, format='text/html')
        self.assertEqual(Post.objects.count(), 1)
        obj = Post.objects.all().first()
        response = self.client.post(reverse('post-update', kwargs={'post_id': obj.id}), self.post, format='text\html')
        self.assertEqual(Post.objects.count(), 1)
        obj = Post.objects.all().first()
        self.assertEqual(obj.title, 'Testtitle')
        self.assertEqual(obj.status, 'PUBLISHED')
