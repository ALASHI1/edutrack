from django.shortcuts import render
from .models import Course
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CourseSerializer, CourseRegistrationSerializer
from permissions.is_teacher import IsTeacher
from permissions.is_student import IsStudent
from drf_yasg.utils import swagger_auto_schema
from utils.decorators import skip_if_swagger


class CreateCourseView(generics.CreateAPIView):
    permission_classes = [IsTeacher]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_summary="Create a course",
        operation_description="Allows a teacher to create a new course."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacherprofile)


class CourseUpdateView(generics.UpdateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_summary="Update your course",
        operation_description="Allows a teacher to update their own course."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @skip_if_swagger(default_return=Course.objects.none())
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user.teacherprofile)


class CourseDeleteView(generics.DestroyAPIView):
    permission_classes = [IsTeacher]
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_summary="Delete your course",
        operation_description="Allows a teacher to delete their own course."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @skip_if_swagger(default_return=Course.objects.none())
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user.teacherprofile)


class AllCourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_summary="List all courses",
        operation_description="Returns a list of all available courses."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_summary="Get course detail",
        operation_description="Retrieve details for a specific course."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class StudentCourseRegisterView(APIView):
    permission_classes = [IsStudent]

    @swagger_auto_schema(
        operation_summary="List all courses for registration",
        operation_description="Returns all courses a student can register for.",
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseRegistrationSerializer,
        operation_summary="Register for a course",
        operation_description="Registers the logged-in student to a selected course using `course_id`."
    )
    def post(self, request):
        serializer = CourseRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            try:
                course = Course.objects.get(pk=course_id)
                course.students.add(request.user.studentprofile)
                course.save()
                return Response({"message": "Successfully registered for the course."})
            except Course.DoesNotExist:
                return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentCourseUnregisterView(APIView):
    permission_classes = [IsStudent]

    @swagger_auto_schema(
        request_body=CourseRegistrationSerializer,
        operation_summary="Unregister from a course",
        operation_description="Allows a student to remove themselves from a registered course using `course_id`."
    )
    def post(self, request):
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({"error": "course_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(pk=course_id)
            course.students.remove(request.user.studentprofile)
            return Response({"message": "Successfully unregistered from the course."})
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)


class StudentCourseListView(generics.ListAPIView):
    permission_classes = [IsStudent]
    serializer_class = CourseSerializer
    filterset_fields = ['title']

    @swagger_auto_schema(
        operation_summary="List enrolled courses",
        operation_description="Returns all courses the logged-in student is currently enrolled in."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @skip_if_swagger(default_return=Course.objects.none())
    def get_queryset(self):
        return Course.objects.filter(students=self.request.user.studentprofile)