from django.shortcuts import render , redirect
from user_app.forms import UserForm, UserProfileInfoForm ,TeacherForm ,UpdateUserForm , UpdateUserProfileInfoForm
from user_app.models import UserProfileInfo, Teacher, Category, Product
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse , HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import user_is_student, user_is_teacher
from django.contrib import messages

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
def register_teacher(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        teacher_form = TeacherForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() and teacher_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors, teacher_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        teacher_form = TeacherForm()

    return render(request, 'user_app/register_teacher.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'teacher_form': teacher_form,
        'registered': registered
    })

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")  # Ambil tipe user dari form

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                # Ambil user profile untuk verifikasi tipe
                try:
                    user_profile = UserProfileInfo.objects.get(user=user)
                except UserProfileInfo.DoesNotExist:
                    return HttpResponse("User profile not found")

                # Verifikasi apakah tipe user sesuai
                if user_type == 'student' and not hasattr(user, 'teacher'):
                    login(request, user)
                    return redirect('user_app:studentdashboard')
                elif user_type == 'teacher' and hasattr(user, 'teacher'):
                    login(request, user)
                    return redirect('user_app:teachersdashboard')
                else:
                    return HttpResponse("Unauthorized access. Invalid user type.")
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
def register_option(request):
    return render(request,'user_app/register_option.html')
    
@login_required
@user_is_student
def studentdashboard(request):
    user_profile = UserProfileInfo.objects.get(user=request.user) # Ambil nama pengguna yang sedang login

    return render(
        request,
        'dashboard_app/student_dashboard.html',
        {
            'user_profile': user_profile,
        }
    )

@login_required
@user_is_student
def studentprofile(request):
    user_profile = UserProfileInfo.objects.get(user=request.user)
    
    # Kirim profil pengguna ke template
    return render(
        request,
        'dashboard_app/student_profile.html',
        {
            'user_profile': user_profile,
        }
    )
@login_required
@user_is_teacher
def teachersdashboard(request):
    teacher_profile = Teacher.objects.get(user = request.user)

    return render(
        request,
        'dashboard_app/teachers_dashboard.html',
        { 'teacher_profile' : teacher_profile}
    )
@login_required
@user_is_teacher
def teacherprofile(request):
    user_profile = UserProfileInfo.objects.get(user=request.user)
    
    # Kirim profil pengguna ke template
    return render(
        request,
        'dashboard_app/teacher_profile.html',
        {
            'user_profile': user_profile,
        }
    )
@login_required
@user_is_teacher
def teacherscourses(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(
        request,
        'dashboard_app/teacherscourses.html', context
    )
@login_required
@user_is_teacher
def productcourses(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        product = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'product' : product, 'category' : category}
        return render(request, "dashboard_app/productcourses.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('teacherscourses')
    
@login_required
@user_is_student
def update_student_profile(request):
    user_profile = UserProfileInfo.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileInfoForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('user_app:studentdashboard'))  # Redirect ke halaman profil
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileInfoForm(instance=user_profile)

    return render(
        request,
        'dashboard_app/update_student_profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )
    
@login_required
@user_is_teacher
def productdetails(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
        if(Product.objects.filter(slug=prod_slug, status=0)):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            context = {'products':products}
        else:
            messages.warning(request, "No such product found")
            return redirect('productcourses')
    else:
        messages.warning(request, "No such category found")
        return redirect('teacherscourses')
    return render(request,"dashboard_app/productdetails.html", context)