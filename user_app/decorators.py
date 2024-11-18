from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def user_is_student(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'userprofileinfo') and not hasattr(request.user, 'teacher'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    return wrapper

def user_is_teacher(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'teacher'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    return wrapper
