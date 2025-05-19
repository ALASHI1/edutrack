from django.urls import path
from apps.courses import views

urlpatterns = [
    path('create/course/', views.CreateCourseView.as_view(), name='create-course'),
    path('courses/', views.AllCourseListView.as_view(), name='course-list'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('course/register/',views.StudentCourseRegisterView.as_view(), name='register-course'),
    path('course/unregister/',views.StudentCourseUnregisterView.as_view(), name='unregister-course'),
    path('course/update/<int:pk>/', views.CourseUpdateView.as_view(), name='update-course'),
    path('course/delete/<int:pk>/', views.CourseDeleteView.as_view(), name='delete-course'),
    
]