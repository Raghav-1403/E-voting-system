from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import CreateUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from main.models import votersdb,minerdb,organizations
from django.contrib.auth.models import User,Group
from .decor import un_user
from client.models import Client
from django.conf import settings
def vews(request):
    settings.SESSION_COOKIE_AGE
    user=request.user
    c=str(user)
    b=None
    bb=None
    if c!= 'AnonymousUser':
        email=request.user.email
        if organizations.objects.filter(author=user).exists():
            b=organizations.objects.get(author=user)
            b=str(b)
            b=b.replace(' ', '.')
            b=b.lower()
        elif minerdb.objects.filter(mail=email).exists():
            for i in user.groups.all():
                if "miner" in str(i):
                    aa=str(i)
                    bb=aa.removeprefix('miner-')
            
    data={'user':user,'b':b,'bb':bb}
    return render(request,"many.html",  data)
@un_user
def register(request):
    vote=votersdb.objects.all()
    form=CreateUser()
    data={'form':form}
    if request.method=='POST':
        form=CreateUser(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            for i in vote:
                if i.mail==email:
                    organ=organizations.objects.get(author=i.author)
                    test=str(organ).replace(' ','.',).lower()
                    group = Group.objects.get(name='voter-'+test)
                    user.groups.add(group)
            messages.success(request,'Successfully register for '+username)
        else:
            messages.warning(request,form.errors)
    return render(request,"register.html",data)
usern=list()
passw=list()
@un_user
def loginUser(request):
    for i in range(len(usern)):
        username=usern[-1]
        password=passw[-1]
        print(username,password)
        user=authenticate(username=username,password=password)
        login(request,user)
        usern.clear()
        passw.clear()
        url="http://localhost:8000/"
        return HttpResponseRedirect(url)    
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('pass')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            b=user.groups.all()
            for i in b:
                aa=str(i)
                if "creator" in str(i): 
                    bb=aa.removeprefix('creator-')
                    usern.append(username)
                    passw.append(password)
                    if str(request.build_absolute_uri())=='http://localhost:8000/login/':
                        url="http://"+bb+".localhost:8000/login/"
                        return HttpResponseRedirect(url)
                    else:
                        return redirect("http://localhost:8000/login/")
                elif "miner" in aa:
                    bb=aa.removeprefix('miner-')
                    usern.append(username)
                    passw.append(password)
                    if str(request.build_absolute_uri())=='http://localhost:8000/login/':
                        url="http://"+bb+".localhost:8000/login/"
                        return HttpResponseRedirect(url)
                    else:
                        return redirect("http://localhost:8000/login/")
                elif "voter" in aa:
                    a=request.build_absolute_uri()
                    if '/login/' in a:
                        a=a.replace("/login/?next=","")
                        return redirect(a)
            else:
                usern.clear()
                passw.clear()
                return redirect("http://localhost:8000/")
        else:
            messages.error(request,"Wrong Credentials!!!")

        
    return render(request,"login.html")
def LogoutUser(request):
    user=request.user
    logout(request)
    if str(request.build_absolute_uri())=='http://localhost:8000/logout/':
        b=user.groups.all()
        for i in b:
            if "creator" in str(i):
                aa=str(i)
                bb=aa.removeprefix('creator-')
                url="http://"+bb+".localhost:8000/logout/"
                return redirect(url)
            elif "miner" in str(i):
                aa=str(i)
                bb=aa.removeprefix('miner-')
                url="http://"+bb+".localhost:8000/logout/"
                return redirect(url)
    elif str(request.build_absolute_uri())!="http://localhost:8000/logout/" :
        logout(request)
        url='http://localhost:8000/logout/'
        return redirect(url)

    return redirect("http://localhost:8000/")
def demouser(request):
    return redirect("http://localhost:8000/logout/")
