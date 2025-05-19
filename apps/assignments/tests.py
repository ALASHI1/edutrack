from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from apps.accounts.models import StudentProfile, TeacherProfile
from apps.courses.models import Course
from apps.assignments.models import Assignment, Submission

class AssignmentSubmissionTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(username='student1', password='pass123')
        self.teacher_user = User.objects.create_user(username='teacher1', password='pass123')

        self.student_profile = StudentProfile.objects.create(user=self.student_user)
        self.teacher_profile = TeacherProfile.objects.create(user=self.teacher_user)

        self.course = Course.objects.create(title='Science', teacher=self.teacher_profile)
        self.course.students.add(self.student_profile)

        self.assignment = Assignment.objects.create(
            title='Lab Report',
            description='Submit your experiment results.',
            due_date='2025-12-31T23:59:00Z',
            course=self.course
        )

        self.submit_url = reverse('submit-assignment')

    def test_student_can_submit_assignment(self):
        self.client.force_authenticate(user=self.student_user)
        data = {
            'assignment': self.assignment.id,
            'content': 'My lab results...',
            'student': self.student_profile.id
        }
        response = self.client.post(self.submit_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Submission.objects.filter(assignment=self.assignment, student=self.student_profile).exists())

    def test_unauthenticated_submission_fails(self):
        data = {
            'assignment': self.assignment.id,
            'content': 'Unauthorized attempt'
        }
        response = self.client.post(self.submit_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_submission_fails(self):
        Submission.objects.create(assignment=self.assignment, student=self.student_profile, content='Initial submit')
        self.client.force_authenticate(user=self.student_user)
        data = {
            'assignment': self.assignment.id,
            'content': 'Second try'
        }
        response = self.client.post(self.submit_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Submission.objects.filter(assignment=self.assignment, student=self.student_profile).count(), 1)

    def test_submission_missing_assignment_fails(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(self.submit_url, {'content': 'Missing assignment ID'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GradeAssignmentTests(APITestCase):

    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher1', password='pass123')
        self.student_user = User.objects.create_user(username='student1', password='pass123')

        self.teacher_profile = TeacherProfile.objects.create(user=self.teacher_user)
        self.student_profile = StudentProfile.objects.create(user=self.student_user)

        self.course = Course.objects.create(title='Physics', teacher=self.teacher_profile)
        self.course.students.add(self.student_profile)

        self.assignment = Assignment.objects.create(
            title='Force & Motion',
            description='Solve all problems.',
            due_date='2025-12-31T23:59:00Z',
            course=self.course
        )

        self.submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student_profile,
            content='Here are my answers.'
        )

        self.grade_url = reverse('grade-assignment', args=[self.submission.id])

    def test_teacher_can_grade_submission(self):
        self.client.force_authenticate(user=self.teacher_user)
        data = {'grade': 'A+'}
        response = self.client.post(self.grade_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.grade, 'A+')
        self.assertTrue(self.submission.reviewed)

    def test_student_cannot_grade_submission(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'grade': 'B'}
        response = self.client.post(self.grade_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_grade_nonexistent_submission(self):
        self.client.force_authenticate(user=self.teacher_user)
        url = reverse('grade-assignment', args=[999])
        response = self.client.post(url, {'grade': 'C'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
        
class DuplicateSubmissionTest(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(username='student1', password='pass123')
        self.teacher_user = User.objects.create_user(username='teacher1', password='pass123')

        self.student_profile = StudentProfile.objects.create(user=self.student_user)
        self.teacher_profile = TeacherProfile.objects.create(user=self.teacher_user)

        self.course = Course.objects.create(title='Biology', teacher=self.teacher_profile)
        self.course.students.add(self.student_profile)

        self.assignment = Assignment.objects.create(
            title='Cell Division',
            description='Describe mitosis.',
            due_date='2025-12-31T23:59:00Z',
            course=self.course
        )

        self.submit_url = reverse('submit-assignment')  # your actual URL name

        # first valid submission
        self.submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student_profile,
            content="First and only answer"
        )

    def test_duplicate_submission_is_rejected(self):
        self.client.force_authenticate(user=self.student_user)
        data = {
            "assignment": self.assignment.id,
            "content": "Trying again"
        }
        response = self.client.post(self.submit_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Submission.objects.filter(assignment=self.assignment, student=self.student_profile).count(), 1)