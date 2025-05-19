from rest_framework import serializers
from .models import Assignment, Submission
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError



class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'course', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'content', 'file', 'link', 'submitted_at', 'reviewed', 'grade']
        read_only_fields = ['id', 'submitted_at', 'reviewed','grade']
        
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError("You have already submitted this assignment.")
        

class GradeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        read_only_fields = ['id', 'assignment', 'student', 'content', 'file', 'link', 'submitted_at', 'reviewed']
        fields = ['grade']