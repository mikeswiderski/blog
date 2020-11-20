from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.users.models import Profile


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.username = 'testusername'
        self.password = 'testpassword'
        self.user = {
            'username': 'testusername',
            'email': 'testemail@gmail.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        return super().setUp()


class RegisterTest(BaseTest):

    def test_can_register_user(self):
        response = self.client.post(
            self.register_url,
            self.user,
            format='text/html',
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.is_active, True)

    def test_password_no_match(self):
        user_credentials = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password1': 'testpassword1',
            'password2': 'testpassword',
        }
        response = self.client.post(
            self.register_url,
            user_credentials,
            format='text/html',
        )
        self.assertRaisesMessage(
            ValueError, "The two password fields didn't match."
        )
        self.assertEqual(User.objects.count(), 0)

    def test_register_no_password(self):
        user_credentials = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password1': '',
            'password2': '',
        }
        response = self.client.post(
            self.register_url,
            user_credentials,
            format='text/html',
        )
        self.assertEqual(User.objects.count(), 0)

    def test_register_no_email(self):
        user_credentials = {
            'username': 'testuser',
            'email': '',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(
            self.register_url,
            user_credentials,
            format='text/html',
        )
        self.assertEqual(User.objects.count(), 0)

    def test_register_no_username(self):
        user_credentials = {
            'username': '',
            'email': 'test@gmail.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(
            self.register_url,
            user_credentials,
            format='text/html',
        )
        self.assertEqual(User.objects.count(), 0)

    def test_user_same_username(self):
        user_credentials = {
            'username': 'testusername',
            'email': 'test@gmail.com',
            'password': 'testpassword',
        }
        user = User.objects.create_user(**user_credentials)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(
            self.register_url,
            self.user,
            format='text/html',
        )
        self.assertRaisesMessage(
            ValueError, "A user with that username already exists."
        )
        self.assertEqual(User.objects.count(), 1)

    def test_user_same_email(self):
        user_credentials = {
            'username': 'differentusername',
            'email': 'testemail@gmail.com',
            'password': 'testpassword',
        }
        user = User.objects.create_user(**user_credentials)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(
            self.register_url,
            self.user,
            format='text/html',
        )
        self.assertRaisesMessage(
            ValueError,
            "This email has already been used. Please use another email."
        )
        self.assertEqual(User.objects.count(), 1)

    def test_user_same_password(self):
        user_credentials = {
            'username': 'differentusername',
            'email': 'differentemail@gmail.com',
            'password': 'testpassword',
        }
        user = User.objects.create_user(**user_credentials)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(
            self.register_url,
            self.user,
            format='text/html',
        )
        self.assertEqual(User.objects.count(), 2)


class LoginTest(BaseTest):

    def test_login_success(self):
        user_credentials = {
            "username": "testusername",
            "password": "testpassword",
        }
        user = User.objects.create_user(**user_credentials)
        user.is_active = True
        user.save()
        response = self.client.post(
            self.login_url,
            user_credentials,
            format='text/html',
        )
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertEqual(int(session.get('_auth_user_id')), user.id)

    def test_login_one_required_field_missing(self):
        user_credentials = {
            "username": "testusername",
            "password": "testpassword",
        }
        user_credentials2 = {
            "username": "testusername",
            "password": "",
        }
        user = User.objects.create_user(**user_credentials)
        user.is_active = True
        user.save()
        response = self.client.post(
            self.login_url,
            user_credentials2,
            format='text/html',
        )
        self.assertRaisesMessage(
            ValueError,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertEqual((session.get('_auth_user_id')), None)

    def test_login_inactive_user(self):
        user_credentials = {
            "username": "testusername",
            "password": "testpassword",
        }
        user = User.objects.create_user(**user_credentials)
        user.is_active = False
        user.save()
        response = self.client.post(
            self.login_url,
            user_credentials,
            format='text/html',
        )
        self.assertRaisesMessage(
            ValueError,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertEqual((session.get('_auth_user_id')), None)

    def test_login_user_invalid_password(self):
        user_credentials = {
            "username": "testusername",
            "password": "testpassword",
        }
        user_credentials2 = {
            "username": "testusername",
            "password": "invalidpassword",
        }
        user = User.objects.create_user(**user_credentials)
        user.is_active = True
        user.save()
        response = self.client.post(
            self.login_url,
            user_credentials2,
            format='text/html',
        )
        self.assertRaisesMessage(
            ValueError,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertEqual((session.get('_auth_user_id')), None)

    def test_login_user_does_not_exist(self):
        user_credentials = {
            "username": "testusername",
            "password": "testpassword",
        }
        user_credentials2 = {
            "username": "testusername_doesnot_exist",
            "password": "testpassword",
        }
        user = User.objects.create_user(**user_credentials)
        user.is_active = True
        user.save()
        response = self.client.post(
            self.login_url,
            user_credentials2,
            format='text/html',
        )
        self.assertRaisesMessage(
            ValueError,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertEqual((session.get('_auth_user_id')), None)

class ProfileTest(BaseTest):

    def test_registered_user_has_profile_created(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.is_active, True)
        self.assertEqual(Profile.objects.count(), 1)
