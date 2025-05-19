from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'students', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at','students','teacher']
        
        
class CourseRegistrationSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(required=True)