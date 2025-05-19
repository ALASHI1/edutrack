from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from apps.accounts.models import StudentProfile, TeacherProfile
from apps.courses.models import Course

class CourseRegistrationTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(username='student1', password='pass123')
        self.teacher_user = User.objects.create_user(username='teacher1', password='pass123')

        self.student_profile = StudentProfile.objects.create(user=self.student_user)
        self.teacher_profile = TeacherProfile.objects.create(user=self.teacher_user)

        self.course = Course.objects.create(title='Test Course', teacher=self.teacher_profile)
        self.register_url = reverse('register-course')

    def test_student_can_register_for_course(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(self.register_url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.student_profile, self.course.students.all())

    def test_register_without_auth_fails(self):
        response = self.client.post(self.register_url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_with_invalid_course_fails(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(self.register_url, {'course_id': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_register_without_course_id_fails(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(self.register_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
