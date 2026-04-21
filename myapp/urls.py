from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/register/', views.student_register, name='student_register'),
    path('courses/register/', views.course_register, name='course_register'),
    path('report/', views.report, name='report'),
]
