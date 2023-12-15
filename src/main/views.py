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
from exp.decor import convertor

# Create your views here.

@login_required(login_url='login')
def homepage(request):
    user=request.user
    org=organizations.objects.get(author=user)
    voters_db=votersdb.objects.filter(org=org).count()
    positions=position.objects.all()
    party_mem,first_pos="",position.objects.first()

    if first_pos is not None:
        first_pos=first_pos.participant
    if request.method=='POST':
        first_pos=request.POST.get('parti')
    if first_pos is not None:
        party_mem=partymembers.objects.filter(party_pos=position.objects.get(participant=first_pos))

    party_1,count_1,temp,par_count,par_count2,party_2,count_2=[],[],[],[],[],[],[]
    temp.append('voter')
    temp.append('value')
    par_count.append(temp)
    temp,total=[],0
    party_2.append('voter')
    count_2.append('value')

    for i in party_mem:
        vote_count,total_count=count.objects.filter(cou=i.party).count(),count.objects.all().count()
        party_1.append(i.party)
        count_1.append(vote_count)
        temp.append(str(i.party))
        if voters_db>0 and total_count>0:
            total+=float(vote_count/voters_db)*100
            temp.append(float(vote_count/total_count)*100)
            count_2.append(float(vote_count/voters_db)*100)
        par_count.append(temp)
        temp=[]

    count_2.append(100-total)
    party_2.extend(party_1)
    party_2.append('Not voted')
    par_count2.append(party_2)
    par_count2.append(count_2)
    data={'org':org,'party_1':party_1,'count_1':count_1,'positions':positions,
    'first_pos':first_pos,'par_count':par_count,'par_count2':par_count2}
    return render(request,"home.html",data)


@login_required(login_url='login')
def creatorpage(request):
    user=request.user
    org=organizations.objects.get(author=user)
    party_mem=partymembers.objects.all()
    positions=position.objects.all()
    data={'party_mem':party_mem,'positions':positions,'org':org}
    
    if request.method=='POST':
        party_name=request.POST.get('names')
        party_disp=request.POST.get('display')
        delete=request.POST.getlist('delete')
        pos=request.POST.get('parti')
        if party_name!=None:
            x=partymembers(party=party_name,party_display=party_disp,party_pos=position.objects.get(participant=pos))
            x.save()
        if delete!=None:
            for i in delete:
                if partymembers.objects.filter(party=i).exists():
                    x=partymembers.objects.filter(party=i)
                    x.delete()
            return redirect('main')
        
    return render(request,"create.html",data)

@login_required(login_url='login')
def startpage(request):
    user=request.user
    positions=position.objects.all()
    org=organizations.objects.get(author=user)
    
    if request.method=='POST':
        pos=request.POST.get('place')
        if pos is not None:
            y=position(participant=pos,org=organizations.objects.get(author=user))
            y.save()
        delete=request.POST.getlist('del')
        if delete is not None:
            for i in delete:
                j=position.objects.get(participant=i)
                j.delete()
            return redirect("start")
   
            
    data={'positions':positions,'org':org}
    return render(request,"init.html",data)

@login_required(login_url='login')
def votersreg(request):
    user=request.user
    org=organizations.objects.get(author=user)
    positions=position.objects.all()
    voters_db=votersdb.objects.filter(org=org)
    data={'voters_db':voters_db,'positions':positions,'org':org}
    temp=convertor(org)
    if Group.objects.filter(name="voter-"+temp).exists():
        pass
    else:
        g=Group(name="voter-"+temp)
        g.save()

    if request.method=='POST':
        name=request.POST.get('name')
        mail=request.POST.get('email')
        pos=request.POST.getlist('check')
        delete=request.POST.getlist('delete')
        
        if name and mail and pos is not None:
            if votersdb.objects.filter(org=org,mail=mail.lower()).exists():
                i=votersdb.objects.get(org=org,mail=mail.lower())
                i.delete()
            user_pos,voted=[],[]
            for i in pos:
                user_pos.append(i)
                voted.append(False)
            x=votersdb(Name=name,mail=mail.lower(),org=org,pos=user_pos,votepos=voted)
            x.save()
            if User.objects.filter(email=mail).exists():
                use=User.objects.get(email=b)
                group = Group.objects.get(name='voter-'+temp)
                use.groups.add(group)
            return redirect('setup')

        if delete is not None:
            for i in delete:
                j=votersdb.objects.get(mail=i)
                j.delete()

    return render(request,"setup.html",data)

@login_required(login_url='login')
def minersreg(request):
    user=request.user
    org=organizations.objects.get(author=user)
    miner_db=minerdb.objects.filter(org=org)
    data={'miner_db':miner_db,'org':org}
    temp=convertor(org)
    if Group.objects.filter(name="miner-"+temp).exists():
        pass
    else:
        g=Group(name="miner-"+temp)
        g.save()

    if request.method=='POST':
        name=request.POST.get('name')
        mail=request.POST.get('email')
        delete=request.POST.getlist('delete')
        if minerdb.objects.filter(mail=mail).exists():
            pass
        else:
            if User.objects.filter(email=mail).exists():
                use=User.objects.get(email=mail)
                group = Group.objects.get(name='miner-'+temp)
                use.groups.add(group)

            if name and mail is not None:
                m=minerdb(Name=name,mail=mail.lower(),org=org,voteval=False)
                m.save()  

        if delete is not None:
            for i in delete:
                j=minerdb.objects.get(mail=i)
                j.delete()

    return render(request,"mineup.html",data)
            
@login_required(login_url='login')
def demopage(request):
    user=request.user
    groups=user.groups.all()
    http=str(request.build_absolute_uri())

    for i in groups:
        i=str(i)
        if 'miner' in i:
            return HttpResponse("Sorry You're not able to create a account please change your profile from miner")
        elif 'creator' in i:
            bb=i.removeprefix('creator-')
            http=http.removeprefix("http://")
            http="http://"+bb+"."+http
            return redirect(http)

    if request.method=='POST':
        org=request.POST.get('org')
        temp=organizations(org=org,author=user)
        temp.save()
        temp=convertor(temp)
        temp=temp.rstrip()
        g=Group(name="creator-"+temp)
        g.save()
        a=Client(schema_name=temp,name=temp)
        a.save()
        b=Domain(domain=temp+".localhost",tenant=Client.objects.get(name=temp),is_primary=True)
        b.save()
        group = Group.objects.get(name='creator-'+temp)
        user.groups.add(group)
        logout(request)
        return redirect('home')

    return render(request,"demo.html")


