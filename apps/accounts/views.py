from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import TeacherProfile, StudentProfile
from .serializers import TeacherProfileSerializer, StudentProfileSerializer

class UpdateTeacherProfileView(generics.UpdateAPIView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    @swagger_auto_schema(
        operation_summary="Update your teacher profile",
        operation_description="Allows a logged-in teacher to update their own profile details."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(TeacherProfile, user=self.request.user)


class TeacherProfileListView(generics.ListAPIView):
    queryset = TeacherProfile.objects.filter(active=True)
    serializer_class = TeacherProfileSerializer

    @swagger_auto_schema(
        operation_summary="List active teacher profiles",
        operation_description="Returns a list of all active teachers in the system."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TeacherProfileDetailView(generics.RetrieveAPIView):
    queryset = TeacherProfile.objects.filter(active=True)
    serializer_class = TeacherProfileSerializer

    @swagger_auto_schema(
        operation_summary="Get your teacher profile",
        operation_description="Fetches the logged-in teacher's profile information."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(TeacherProfile, user=self.request.user)

class UpdateStudentProfileView(generics.UpdateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    @swagger_auto_schema(
        operation_summary="Update your student profile",
        operation_description="Allows a logged-in student to update their own profile details."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(StudentProfile, user=self.request.user)


class StudentProfileListView(generics.ListAPIView):
    queryset = StudentProfile.objects.filter(active=True)
    serializer_class = StudentProfileSerializer

    @swagger_auto_schema(
        operation_summary="List active student profiles",
        operation_description="Returns a list of all active students in the system."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class StudentProfileDetailView(generics.RetrieveAPIView):
    queryset = StudentProfile.objects.filter(active=True)
    serializer_class = StudentProfileSerializer

    @swagger_auto_schema(
        operation_summary="Get your student profile",
        operation_description="Fetches the logged-in student's profile information."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(StudentProfile, user=self.request.user)
