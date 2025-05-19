from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from apps.accounts.models import StudentProfile, TeacherProfile


class AuthTests(APITestCase):

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "first_name": "Test",
            "last_name": "User",
            "is_teacher": True
        }
        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        self.test_user_registration()
        data = {
            "username": "testuser",
            "password": "StrongPass123"
        }
        response = self.client.post(reverse('rest_login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_logout(self):
        self.test_user_login()
        response = self.client.post(reverse('rest_logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileViewTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(username='student1', password='pass123')
        self.teacher_user = User.objects.create_user(username='teacher1', password='pass123')

        self.student_profile = StudentProfile.objects.create(
            user=self.student_user,
            student_id="S001",
        )

        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_id="T001"
        )

        self.student_url = reverse('student-profile')  
        self.teacher_url = reverse('teacher-profile')

    def test_student_can_view_own_profile(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.student_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_id'], 'S001')

    def test_teacher_can_view_own_profile(self):
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(self.teacher_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee_id'], 'T001')

    def test_unauthenticated_access_fails(self):
        response = self.client.get(self.student_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#Course registration

#  Assignment submission

#  Grade assignment

#  List own profile

#  Prevent duplicate submissions