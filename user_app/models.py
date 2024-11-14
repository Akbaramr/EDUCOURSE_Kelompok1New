from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    # Membuat relasi ( tidak menurun dari user!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # membuat attribut apa saja yang ingin user masukkan
    portofolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    # Membuat __str__ method untuk override yang default
    def __str__(self):
        # Built in attribute of django.contrib.auth.models.User
        return self.user.username


