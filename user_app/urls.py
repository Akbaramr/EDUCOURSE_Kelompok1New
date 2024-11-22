from django.urls import path
from user_app import views

app_name = 'user_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register_teacher/', views.register_teacher, name='register_teacher'),
    path('register_option/', views.register_option, name='register_option'),
    path('user_login/', views.user_login, name='user_login'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('student', views.student, name='student'),
    path('teacher', views.teacher, name='teacher'),
    path('faq', views.faq, name='faq'),
    path('contact', views.contact, name='contact'),    
    path('studentdashboard', views.studentdashboard, name='studentdashboard'),
    path('studentprofile',views.studentprofile, name='studentprofile'),
    path('teachersdashboard', views.teachersdashboard, name='teachersdashboard'),
    path('teacherprofile',views.teacherprofile, name='teacherprofile'),
    path('teacherscourses', views.teacherscourses, name='teacherscourses'),
    path('teacherscourses/<str:slug>', views.productcourses, name='productcourses'),
    path('student/profile/update/', views.update_student_profile, name='update_student_profile'),
]
