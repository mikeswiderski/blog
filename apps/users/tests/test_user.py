from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User

 
class BaseTest(TestCase):
    def setUp(self):
        self.client=Client()
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.user={
            'username':'testusername', 
            'email':'testemail@gmail.com', 
            'password1':'testpassword', 
            'password2':'testpassword'
        }
        return super().setUp() 

class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response=self.client.get(self.register_url) 
        self.assertEqual(response.status_code,200) 
        self.assertTemplateUsed(response,'users/register.html')

    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

class LoginTest(BaseTest):
    def test_can_access_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200) 
        self.assertTemplateUsed(response,'users/login.html')

    '''
    def test_login_success(self):
        self.client.post(self.register_url,self.user,format='text/html')
        user=User.objects.filter(username=self.user['username']).first()
        user.is_active=True
        user.save()
        response=self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)'''

    def test_login_success(self):
        user = User.objects.create_user(username='testusername', password='testpassword')
        user.is_active=True
        user.save()
        response=self.client.post(self.login_url,{'username':'testusername', 'password':'testpassword'},format='text/html')
        self.assertEqual(response.status_code,302)
