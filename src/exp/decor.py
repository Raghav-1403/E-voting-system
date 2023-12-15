from django.http import HttpResponse
from django.shortcuts import redirect
def un_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            http=str(request.build_absolute_uri())
            dom,host=http.split('localhost:')
            host=list(host.split('/'))
            host=host[0]
            return redirect("http://localhost:"+host)
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

def convertor(temp):
    temp=str(temp)
    temp=temp.replace(' ', '.')
    temp=temp.lower()
    return temp