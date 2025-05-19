from django.contrib import admin
from apps.accounts.models import TeacherProfile, StudentProfile
# Register your models here.


admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)