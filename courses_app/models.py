from django.db import models
from django.utils import timezone
from django.urls import reverse 
from embed_video.fields import EmbedVideoField
from user_app.models import Teacher

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='thumbnail',blank=True)
    video = EmbedVideoField(blank=True, null=True)  # Tambahkan field untuk video
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})
    
    def __str__(self):
        return self.title