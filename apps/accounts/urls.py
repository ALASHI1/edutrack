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


# Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3ODU1NTI3LCJpYXQiOjE3NDc1OTYzMjcsImp0aSI6IjMzMTA3NmUzMjZiNDQzODFhZGM4MTEyYmUyZDkxNjcxIiwidXNlcl9pZCI6MX0.BTN5-35fOyjzTdRsfnNaCB1bDrmy70W1QXHc7vPXexs