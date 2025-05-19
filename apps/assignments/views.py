from django.shortcuts import get_object_or_404
from .models import Assignment, Submission
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSubmissionSerializer
from permissions.is_teacher import IsTeacher
from permissions.is_student import IsStudent
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied



class CreateAssignmentView(generics.CreateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = AssignmentSerializer

    @swagger_auto_schema(
        operation_summary="Create an assignment",
        operation_description="Allows a teacher to create a new assignment for a course."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return Assignment.objects.filter(course__teacher=self.request.user.teacherprofile)

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if course.teacher != self.request.user.teacherprofile:
            raise PermissionDenied("You can only create assignments for your own courses.")
        serializer.save()
        
class UpdateAssignmentView(generics.UpdateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = AssignmentSerializer

    @swagger_auto_schema(
        operation_summary="Update an assignment",
        operation_description="Allows a teacher to update an existing assignment."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get_queryset(self):
        return Assignment.objects.filter(course__teacher=self.request.user.teacherprofile)
    
    
class DeleteAssignmentView(generics.DestroyAPIView):
    permission_classes = [IsTeacher]
    serializer_class = AssignmentSerializer

    @swagger_auto_schema(
        operation_summary="Delete an assignment",
        operation_description="Allows a teacher to delete an existing assignment."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Assignment.objects.filter(course__teacher=self.request.user.teacherprofile)
   


class TeacherAllAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacher]
    filterset_fields = ['course']

    @swagger_auto_schema(
        operation_summary="List all assignments by course",
        operation_description="Fetch all assignments created for a specific course."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Assignment.objects.filter(course__id=course_id)


class TeacherAssignmentSubmissionUngraded(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsTeacher]
    filterset_fields = ['assignment__course']   

    @swagger_auto_schema(
        operation_summary="List ungraded submissions",
        operation_description="List all assignment submissions that have not been reviewed for a given course."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Submission.objects.filter(
            assignment__course_id=course_id,
            reviewed=False
        ).select_related('assignment', 'student')


class TeacherAssignmentSubmissionGraded(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsTeacher]
    filterset_fields = ['assignment__course']
    
    @swagger_auto_schema(
        operation_summary="List graded submissions",
        operation_description="List all assignment submissions that have been reviewed for a given course."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Submission.objects.filter(
            assignment__course_id=course_id,
            reviewed=True
        ).select_related('assignment', 'student')


class GradeAssignmentView(APIView):
    serializer_class = GradeSubmissionSerializer
    permission_classes = [IsTeacher]

    @swagger_auto_schema(
        operation_summary="Get a submission for grading",
        operation_description="Retrieve a specific submission to view its content before grading."
    )
    def get(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            serializer = self.serializer_class(submission)
            return Response(serializer.data)
        except Submission.DoesNotExist:
            return Response({"error": "Submission not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=GradeSubmissionSerializer,
        operation_summary="Grade a submission",
        operation_description="Allows a teacher to provide a grade and mark a submission as reviewed."
    )
    def post(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            serializer = self.serializer_class(submission, data=request.data, partial=True)
            if serializer.is_valid():
                instance = serializer.save()
                instance.reviewed = True
                instance.save()
                return Response(self.serializer_class(instance).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Submission.DoesNotExist:
            return Response({"error": "Submission not found."}, status=status.HTTP_404_NOT_FOUND)


class StudentPendingAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudent]
    filterset_fields = ['course']
    

    @swagger_auto_schema(
        operation_summary="List pending assignments (by course)",
        operation_description="Lists assignments in a course that the student has not yet submitted."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course_assignments = Assignment.objects.filter(course_id=course_id, course__students=self.request.user.studentprofile)
        submitted_assignments = Submission.objects.filter(
            student__user=self.request.user,
            assignment__course_id=course_id
        ).values_list('assignment_id', flat=True)
        return course_assignments.exclude(id__in=submitted_assignments)


class StudentAllPendingAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudent]
    filterset_fields = ['course']

    @swagger_auto_schema(
        operation_summary="List all pending assignments",
        operation_description="Lists all assignments across enrolled courses that the student has not yet submitted."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course_assignments = Assignment.objects.filter(course__students=self.request.user.studentprofile)
        submitted_assignments = Submission.objects.filter(
            student__user=self.request.user
        ).values_list('assignment_id', flat=True)
        return course_assignments.exclude(id__in=submitted_assignments)


class StudentSubmittedAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudent]
    filterset_fields = ['course']

    @swagger_auto_schema(
        operation_summary="List submitted assignments (by course)",
        operation_description="Lists all assignments submitted by the student in a specific course."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Submission.objects.filter(
            student__user=self.request.user,
            assignment__course_id=course_id
        ).select_related('assignment')


class SubmitAssignmentView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]

    @swagger_auto_schema(
        operation_summary="Submit an assignment",
        operation_description="Allows a student to submit a response for an assignment."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.studentprofile)
