from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('home/', views.job_list, name='home'),
    path('login/', views.user_login, name='login'),  # Updated
    path('register/', views.register, name='register'),
    path('job/<int:id>/', views.job_detail, name='job_detail'),
    path('apply/<int:id>/', views.apply_job, name='apply_job'),
    path('post-job/', views.post_job, name='post_job'),
]
