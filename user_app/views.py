from django.shortcuts import render
from user_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "user_app/index.html")

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # Hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user  # OneToOne relationship

            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(
        request,
        "user_app/register.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Get from login.html
        password = request.POST.get("password")  # Get from login.html

        user = authenticate(request,username=username, password=password)

        if user:
            if user.is_active:
                login(request , user)
                return render(request,'dashboard_app/student_dashboard.html')
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print(f"Username: {username} and password: {password}")
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, "user_app/login.html", {})
    
def contact(request):
    return render(request,'user_app/contact.html')
def about(request):
    return render(request,'user_app/aboutus.html')
def student(request):
    return render(request,'user_app/student.html')
def teacher(request):
    return render(request,'user_app/teacher.html')
def faq(request):
    return render(request,'user_app/faq.html')
    
@login_required
def studentdashboard(request):
    username = request.user.username  # Ambil nama pengguna yang sedang login
    user_name = {
        'username': username,
    }
    return render(request, 'dashboard_app/student_dashboard.html', context = user_name)