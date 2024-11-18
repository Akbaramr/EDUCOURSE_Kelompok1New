from django.contrib import admin
from user_app.models import UserProfileInfo ,Teacher

# Register your models here.
admin.site.register(UserProfileInfo)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject_taught', 'experience')
    search_fields = ('user__username', 'subject_taught')

admin.site.register(Teacher, TeacherAdmin)