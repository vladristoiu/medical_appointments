from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, SESSION_KEY
from appointments.models import Token

class AuthenticationTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.token = Token.objects.create(number='12345', user=self.user)

    def test_valid_user_login(self):
        response = self.client.post(reverse('authentication-view'), self.credentials, follow=True)
        self.assertRedirects(response, reverse('verify-view'))
        self.assertEqual(self.client.session['pk'], self.user.pk)

    def test_invalid_user_login(self):
        invalid_credentials = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('authentication-view'), invalid_credentials, follow=True)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_unauthenticated_user_verify_view_access(self):
        response = self.client.get(reverse('verify-view'))
        self.assertRedirects(response, reverse('authentication-view'))

    def test_wrong_token_verification(self):
        self.client.post(reverse('authentication-view'), self.credentials, follow=True)
        response = self.client.post(reverse('verify-view'), {'number': 'wrongtoken'}, follow=True)
        self.assertNotIn(SESSION_KEY, self.client.session)

