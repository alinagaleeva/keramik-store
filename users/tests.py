from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from .models import EmailVerification, User


class UserLoginViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.path = reverse('login')

    def test_login_page_loads_successfully(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_successful(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # self.assertRedirects(response, reverse('profile'))

    def test_login_failure(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertTrue(response.context['form'].errors)


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Alina', 'last_name': 'Galeeva',
            'username': 'alinatest', 'email': 'alina-galeeva@list.ru',
            'password1': '12345678JNJnjn', 'password2': '12345678JNJnjn',
        }
        self.path = reverse('create_account')

    def test_user_registration(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'create account')
        self.assertTemplateUsed(response, 'users/create_account.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=24)).date()
        )


class ProfileViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.path = reverse('profile')

    def test_profile_view(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response_one = self.client.post(self.path, data)

        self.assertEqual(response_one.status_code, HTTPStatus.FOUND)

        '''response_two = self.client.get(self.path)
        self.assertEqual(response_two.context_data['title'], 'account')
        self.assertTemplateUsed(response_two, 'users/profile.html')'''


'''class OrdersViewTestCase(TestCase):

    def test_profile_view(self):
        path = reverse('orders')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'orders')
        self.assertTemplateUsed(response, 'users/orders.html')'''
