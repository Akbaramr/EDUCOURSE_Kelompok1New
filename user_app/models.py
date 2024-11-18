from django.db import models
from django.contrib.auth.models import User

import datetime
import os
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
    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject_taught = models.CharField(max_length=100)
    experience = models.IntegerField()

    def __str__(self):
        return self.user.username

# laman courses teacher

def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)

class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    desc = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    small_desc = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    desc = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    ori_price = models.FloatField(null=False,blank=False)
    sell_price = models.FloatField(null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
