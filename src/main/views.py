from django.shortcuts import render,redirect,HttpResponse
from user.models import partymembers,position
from .models import votersdb,minerdb,organizations
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from mine.models import count
import json,random
from client.models import Client,Domain
from django.contrib.auth import login,authenticate,logout

email_list=User.objects.values_list("email",flat=True)
# Create your views here.

@login_required(login_url='http://localhost:8000/login/')
def homepage(request):
    user=request.user
    a=organizations.objects.filter(author=user)
    yy=votersdb.objects.filter(author=user).count()
    for i in a:
        break
    else:
        a=None
    vv=position.objects.all()
    b,zz="",position.objects.first()
    if zz is not None:
        zz=zz.participant
    if request.method=='POST':
        zz=request.POST.get('parti')
    if zz is not None:
        b=partymembers.objects.filter(party_pos=position.objects.get(participant=zz))
    forpar,yval=[],[]
    lis1,lis2=[],[]
    lis1.append('voter')
    lis1.append('value')
    lis2.append(lis1)
    lis1=list()
    lis3=list()
    case1,case2=list(),list()
    case1.append('voter')
    case2.append('value')
    total=0
    for i in b:
        c=count.objects.filter(cou=i.party).count()
        full=count.objects.all().count()
        forpar.append(i.party)
        yval.append(c)
        lis1.append(str(i.party))
        if yy>0:
            total+=float(c/yy)*100
            lis1.append(float(c/full)*100)
            case2.append(float(c/yy)*100)
        lis2.append(lis1)
        lis1=list()
    case2.append(100-total)
    case1.extend(forpar)
    case1.append('Not voted')
    lis3.append(case1)
    lis3.append(case2)
    print(lis3)
    return render(request,"home.html",{'a':a,'forpar':forpar,'yval':yval,'vv':vv,'zz':zz,'lis2':lis2,'lis3':lis3})

@login_required(login_url='http://localhost:8000/login/')
def creatorpage(request):
    user=request.user
    z=organizations.objects.all().filter(author=user)
    m=partymembers.objects.all()
    n=position.objects.all()
    data={'m':m,'n':n,'z':z}
    
    if organizations.objects.filter(author=user).exists():
        if request.method=='POST':
            a=request.POST.get('names')
            b=request.POST.get('display')
            c=request.POST.getlist('delete')
            e=request.POST.get('parti')
            if a!=None:
                x=partymembers(party=a,party_display=b,party_pos=position.objects.get(participant=e))
                x.save()
            if c!=None:
                for i in c:
                    for x in m:
                        if i==x.party or i==x.party_display:
                            x.delete()
                return redirect('main')

            data={'a':a,'b':b,'z':z,'m':m,'n':n}
    else:
        return redirect("create")
        
    return render(request,"create.html",data)

@login_required(login_url='http://localhost:8000/login/')
def startpage(request):
    user=request.user
    x=position.objects.all()
    z=organizations.objects.all().filter(author=user)
    if organizations.objects.filter(author=user).exists():
        if request.method=='POST':
            d=request.POST.get('place')
            if d is not None:
                y=position(participant=d,org=organizations.objects.get(author=user))
                y.save()
            f=request.POST.getlist('del')
            if f is not None:
                for i in f:
                    j=position.objects.get(participant=i)
                    j.delete()
                return redirect("start")
    else:
        return redirect("create")
            
    data={'x':x,'z':z}
    return render(request,"init.html",data)

@login_required(login_url='http://localhost:8000/login/')
def votersreg(request):
    user=request.user
    m=User.objects.all()
    z=organizations.objects.all().filter(author=user)
    x=position.objects.all()
    disp=votersdb.objects.all().filter(author=user)
    data={'disp':disp,'x':x,'z':z}
    temp=organizations.objects.get(author=user)
    temp=str(temp)
    temp=temp.replace(' ', '.')
    temp=temp.lower()
    if Group.objects.filter(name="voter-"+temp).exists():
        pass
    else:
        g=Group(name="voter-"+temp)
        g.save()

    if organizations.objects.filter(author=user).exists():
        if request.method=='POST':
            a=request.POST.get('name')
            b=request.POST.get('email')
            c=request.POST.getlist('check')
            delete=request.POST.getlist('delete')
            for i in email_list:
                if i==b:
                    use=User.objects.get(email=b)
                    group = Group.objects.get(name='voter-'+temp)
                    use.groups.add(group)
                    break 
            if a and b and c is not None:
                for i in disp:
                    if i.mail==b:
                        i.delete()
                        break
                li=list()
                votee=list()
                for i in c:
                    li.append(i)
                    votee.append(False)
                x=votersdb(Name=a,mail=b.lower(),author=user,pos=li,votepos=votee)
                x.save()
                return redirect('setup')
                messages.success(request,'Successfully register for '+a)
            elif a and b is None:
                messages.error(request,"Invalid Input")
            if delete is not None:
                for i in delete:
                    j=votersdb.objects.get(mail=i)
                    j.delete()
    else:
        return redirect("create")
    return render(request,"setup.html",data)

@login_required(login_url='http://localhost:8000/login/')
def minersreg(request):
    user=request.user
    z=organizations.objects.all().filter(author=user)
    a=minerdb.objects.all().filter(author=user)
    data={'a':a,'z':z}
    temp=organizations.objects.get(author=user)
    temp=str(temp)
    temp=temp.replace(' ', '.')
    temp=temp.lower()
    if Group.objects.filter(name="miner-"+temp).exists():
        pass
    else:
        g=Group(name="miner-"+temp)
        g.save()
    if organizations.objects.filter(author=user).exists():
        if request.method=='POST':
            c=request.POST.get('name')
            b=request.POST.get('email')
            delete=request.POST.getlist('delete')
            if minerdb.objects.filter(mail=email).exists():
                pass
            else:
                for i in email_list:
                    if i==b:
                        use=User.objects.get(email=b)
                        group = Group.objects.get(name='miner-'+temp)
                        use.groups.add(group)
                if c and b is not None:
                    m=minerdb(Name=c,mail=b.lower(),author=user,voteval=False)
                    m.save()
                    messages.success(request,'Successfully register for '+c)
                elif c and b is None:
                    messages.error(request,"Invalid Input")    
                if delete is not None:
                    for i in delete:
                        j=minerdb.objects.get(mail=i)
                        j.delete()
    else:
        return redirect("create")
    return render(request,"mineup.html",data)
            
@login_required(login_url='http://localhost:8000/login/')
def demopage(request):
    user=request.user
    groups=user.groups.all()
    for i in groups:
        if 'miner' in str(i):
            return HttpResponse("Sorry You're not able to create a account please change your profile from miner")
        elif 'creator' in str(i):
            return HttpResponse("you're already a creator!!!")
    if request.method=='POST':
        organ=request.POST.get('org')
        temp=organizations(org=organ,author=user)
        temp.save()
        temp=str(temp)
        temp=temp.replace(' ', '.')
        temp=temp.lower().rstrip()
        g=Group(name="creator-"+str(temp))
        g.save()
        a=Client(schema_name=str(temp),name=str(temp))
        a.save()
        b=Domain(domain=str(temp)+".localhost",tenant=Client.objects.get(name=str(temp)),is_primary=True)
        b.save()
        group = Group.objects.get(name='creator-'+str(temp))
        user.groups.add(group)
        logout(request)
    return render(request,"demo.html")


