from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.user.models import CustomUser, Otp
from rest_framework.authtoken.models import Token
import uuid
class UserAuthTests(APITestCase):

    def test_user_signup(self):
        """
        Test user signup with valid data and ensure OTP is created.
        """
        url = reverse('v1:sign_up')
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Otp.objects.filter(user__email="testuser@example.com").exists())

    def test_otp_verification(self):
        """
        Test OTP verification and user activation.
        """
        user = CustomUser.objects.create_user(email="testuser2@example.com", password="testpassword123", is_active=False)
        otp_code = '123456'
        Otp.objects.create(user=user, otp=otp_code)

        url = reverse('v1:otp_verify')
        data = {
            "otp": otp_code
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data['results'])
        user.refresh_from_db()
        self.assertTrue(user.is_active) 
        self.assertFalse(Otp.objects.filter(otp=otp_code).exists())  

    def test_user_signin(self):
        """
        Test user sign-in with correct credentials and token generation.
        """
        unique_email = f"{uuid.uuid4()}@example.com"
        user = CustomUser.objects.create_user(email=unique_email, password="testpassword123", is_active=True)
        token = Token.objects.create(user=user)

        print(user.email)
        print(token.key)
        
        url = reverse('v1:sign_in')
        data = {
            "email": unique_email,
            "password": "testpassword123"
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data['results'])
    
    def test_signin_invalid_credentials(self):
        """
        Test user sign-in with incorrect credentials.
        """
        CustomUser.objects.create_user(email="testuser4@example.com", password="testpassword123", is_active=True)
        
        url = reverse('v1:sign_in')
        data = {
            "email": "testuser4@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        

    def test_signin_user_not_exist(self):
        """
        Test sign-in when user does not exist.
        """
        url = reverse('v1:sign_in')
        data = {
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "User does not exist")

