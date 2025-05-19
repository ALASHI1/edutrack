from django.urls import path
from apps.assignments import views

urlpatterns = [
    path('assignment/create/', views.CreateAssignmentView.as_view(), name='create-assignment'),
    path('assignment/update/<int:pk>/', views.UpdateAssignmentView.as_view(), name='update-assignment'),
    path('assignment/delete/<int:pk>/', views.DeleteAssignmentView.as_view(), name='delete-assignment'),
    path('assignments/<int:course_id>/', views.TeacherAllAssignmentListView.as_view(), name='teacher-all-assignments'),
    path('assignments/ungraded/<int:course_id>/', views.TeacherAssignmentSubmissionUngraded.as_view(), name='teacher-assignment-submission-ungraded'),
    path('assignments/graded/<int:course_id>/', views.TeacherAssignmentSubmissionGraded.as_view(), name='teacher-assignment-submission-graded'),
    path('assignments/grade/<int:submission_id>/', views.GradeAssignmentView.as_view(), name='grade-assignment'),
    path('assignment/submit/', views.SubmitAssignmentView.as_view(), name='submit-assignment'),
    path('assignment/submitted/<int:course_id>/', views.StudentSubmittedAssignmentListView.as_view(), name='submitted-assignment'),
    path('assignment/pending/<int:course_id>/', views.StudentPendingAssignmentListView.as_view(), name='pending-assignment'),
    path('assignments/pending/', views.StudentAllPendingAssignmentListView.as_view(), name='student-pending-assignments'),
]