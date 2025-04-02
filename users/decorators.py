from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_login_required():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.session.get("admin_id"):
                return view_func(request, *args, **kwargs)
            messages.error(request, "You are not logged in!")
            return redirect("index") 
        return wrapper
    return decorator

def doctor_login_required():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.session.get("doctor_id"):
                return view_func(request, *args, **kwargs)
            messages.error(request, "You are not logged in!")
            return redirect("index") 
        return wrapper
    return decorator

def patient_login_required():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.session.get("patient_id"):
                return view_func(request, *args, **kwargs)
            messages.error(request, "You are not logged in!")
            return redirect("index") 
        return wrapper
    return decorator