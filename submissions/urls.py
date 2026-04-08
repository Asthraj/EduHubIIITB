from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:id>/', views.submit_assignment, name='submit'),
    path('teacher/submissions/', views.teacher_submissions, name='teacher_submissions'),
    path('teacher/grade/<int:id>/', views.grade_submission, name='grade_submission'),
]
