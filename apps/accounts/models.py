from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"
    

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"