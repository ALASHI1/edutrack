from django.urls import path
from apps.accounts import views

urlpatterns = [
    path('students/', views.StudentProfileListView.as_view(), name='student-list'),
    path('student/profile/', views.StudentProfileDetailView.as_view(), name='student-profile'),
    path('teachers/', views.TeacherProfileListView.as_view(), name='teacher-list'),
    path('teacher/profile/', views.TeacherProfileDetailView.as_view(), name='teacher-profile'),
    path('update/teacher/', views.UpdateTeacherProfileView.as_view(), name='update-teacher-profile'),
    path('update/student/', views.UpdateStudentProfileView.as_view(), name='update-student-profile'),
]