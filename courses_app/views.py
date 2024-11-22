from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_app.decorators import user_is_student, user_is_teacher

# Create your views here.
def index(request):
    return render(request, "user_app/index.html")

@login_required
@user_is_student
def search(request):
    return render(request,'student_courses/search_courses.html')