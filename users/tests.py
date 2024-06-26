import os
from datetime import timedelta

import django
from django.utils.timezone import now

os.environ['DJANGO_SETTINGS_MODULE'] = 'store.settings'
django.setup()

from users.models import User, EmailVerification

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.forms import UserRegistrationForm


# Create your tests here.

class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse("users:registration")

        self.data = {
            "first_name" : "Valt",
            "last_name": "Kas",
            "username": "valee",
            "email": "t@gmail.com",
            "password1": "12345678Ff",
            "password2": "12345678Ff"
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], "Store - Регистрация")
        # self.assertTemplateUsed(response, "users/registration.html")

    def test_user_registration_post_success(self):


        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, data=self.data)

        # creating a user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(username=username).exists())

        # check verification email
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date
            (now() + timedelta(hours=48)).date,
        )

    def test_user_registration_post_error(self):
        username = self.data['username']
        user = User.objects.create(username=username)

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Пользователь с таким именем уже существует",html=True)



