from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import TeacherProfile, StudentProfile

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_teacher = serializers.BooleanField(default=False)
    

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['is_teacher'] = self.validated_data.get('is_teacher', False)
        return data
    
    
class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'employee_id', 'bio', 'active']
        read_only_fields = ['id', 'user','active']
        


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'student_id', 'active']
        read_only_fields = ['id', 'user','active']
        
        
        