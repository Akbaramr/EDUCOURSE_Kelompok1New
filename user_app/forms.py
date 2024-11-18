from django import forms
from django.contrib.auth.models import User
from user_app.models import UserProfileInfo ,Teacher

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta ():
        model = User
        fields = ('username','email','password')
        
class UserProfileInfoForm(forms.ModelForm):
        class Meta ():
            model = UserProfileInfo
            fields = ('portofolio_site','profile_pic')

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('subject_taught', 'experience')