from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import CreateUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from main.models import votersdb,minerdb,organizations
from django.contrib.auth.models import User,Group
from .decor import un_user,convertor
from client.models import Client
from django.conf import settings

def vews(request):
    http=str(request.build_absolute_uri())
    user=request.user
    user_str=str(user)
    org_db,miner_group=None,None
    if '127.0.0.1' in http:
        http=http.replace('127.0.0.1','localhost')
        return redirect(http)
    domain,host=http.split('localhost:')

    if user_str!= 'AnonymousUser':
        email=request.user.email
        if organizations.objects.filter(author=user).exists():
            org_db=organizations.objects.get(author=user)
            org_db=convertor(org_db)
        elif minerdb.objects.filter(mail=email).exists():
            for i in user.groups.all():
                user_group=str(i)
                if "miner" in user_group:
                    miner_group=user_group.removeprefix('miner-')
            
    data={'user':user,'org_db':org_db,'miner_group':miner_group,'http':http,'host':host}
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

            if votersdb.objects.filter(mail=email).exists():
                voter=votersdb.objects.filter(mail=email)
                for i in voter:
                    org_db=i.org
                    test=convertor(org_db)
                    group = Group.objects.get(name='voter-'+test)
                    user.groups.add(group)

            messages.success(request,'Successfully register for '+username)
            
        else:
            messages.warning(request,form.errors)
    return render(request,"register.html",data)

usern,passw,create,miner="","",False,False
@un_user
def loginUser(request):
    http=str(request.build_absolute_uri())
    global usern,passw

    if usern and passw is not None:
        user=authenticate(username=usern,password=passw)
        login(request,user)
        usern,passw="",""
        global create,miner
        if create==True:
            return redirect('create')
        elif miner==True:
            return redirect('mining')  

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('pass')
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            user_group=user.groups.all()
            if "/login/?next=/voters/select/" in http:
                http=http.replace("/login/?next=","")
                return redirect(http)

            for i in user_group:
                str_group,org_name=str(i),''
                if "creator" in str_group or "miner" in str_group:
                    if "creator" in str_group:
                        org_name=str_group.removeprefix('creator-')
                        create=True
                    elif "miner" in str_group:
                        org_name=str_group.removeprefix('miner-')
                        miner=True
                    usern,passw=username,password

                    if http.startswith("http://"+org_name):
                        http=http.removeprefix("http://"+org_name+".")
                        http="http://"+http
                        return HttpResponseRedirect(http)
                    else:
                        http=http.removeprefix("http://")
                        http="http://"+org_name+"."+http
                        return redirect(http)

            else:
                usern,passw='',''
                dom,host=http.split('localhost:')
                host=list(host.split('/'))
                host=host[0]
                return redirect('http://localhost:'+host)
        else:
            messages.error(request,"Wrong Credentials!!!")

    return render(request,"login.html")

def LogoutUser(request):    
    http=str(request.build_absolute_uri())
    user=request.user
    logout(request)
    user_group=user.groups.all()
    for i in user_group:
        str_group,org_name=str(i),''
        
        if "creator" in str_group or "miner" in str_group:
            if "creator" in str_group:
                org_name=str_group.removeprefix('creator-')    
            elif "miner" in str_group:
                org_name=str_group.removeprefix('miner-')

            if http.startswith("http://"+org_name):
                http=http.removeprefix("http://"+org_name+".")
                http="http://"+http
                return HttpResponseRedirect(http)
            else:
                http=http.removeprefix("http://")
                http="http://"+org_name+"."+http
                return redirect(http)

    return redirect('login')
