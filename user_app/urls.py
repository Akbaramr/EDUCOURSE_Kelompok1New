from django.urls import path
from user_app import views

app_name = 'user_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('student', views.student, name='student'),
    path('teacher', views.teacher, name='teacher'),
    path('faq', views.faq, name='faq'),
    path('contact', views.contact, name='contact'),
<<<<<<< HEAD
    path('studentdashboard', views.studentdashboard, name='studentdashboard'),
=======
    path('my_course', views.my_course, name='my_course'),
>>>>>>> 33f4fb80b7df20553d2a6321d5558fccaa521a8d
]
