from django.http import HttpResponse
from django.shortcuts import redirect
def un_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("http://localhost:8000/")
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func