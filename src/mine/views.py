from django.shortcuts import render,HttpResponse,redirect
from user.models import partymembers,hashvalue
from .models import count,track
from main.models import minerdb
from django.contrib.auth.models import User
import hashlib
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def mining(request):
    email=request.user.email
    data={}
    select=""
    if minerdb.objects.filter(mail=email).exists():
        select=minerdb.objects.get(mail=email)
    else:
        return HttpResponse("sorry you're not authenticated ")
    hash_last=hashvalue.objects.last()
    data={'hash_last':hash_last}
    tracks=track.objects.last()
    prev=''
    hash_id=hash_last.id
    if tracks is not None:
        tracks=tracks.trace
        prevhash=hashvalue.objects.get(id=tracks)
        prev=prevhash.hash_values
    else:
        tracks=0
    
    if request.method=='POST':
        if tracks!=hash_id:
            part_mem=partymembers.objects.all()
            last_val=hash_last.hash_values
            for j in part_mem:
                vote=j.party
                z="_"+vote+"-"+prev+"_"
                hashed=hashlib.sha256(z.encode()).hexdigest()
                if last_val==hashed:
                    m=count(cou=vote)
                    m.save()
                    break   
            h=track(trace=hash_id)
            h.save()
        select.voteval=True
        select.save()
        last_vote=count.objects.last()
        data={'last_vote':last_vote,'hash_last':hash_last}
    return render(request,"miner.html",data)

@login_required(login_url='login')
def demomine(request):
    user=request.user
    groups=user.groups.all()
    http=str(request.build_absolute_uri())
    for i in groups:
        i=str(i)
        if 'miner' in i:
            bb=i.removeprefix('miner-')
            http=http.removeprefix("http://")
            http="http://"+bb+"."+http
            return redirect(http)
    else:
        return HttpResponse("sorry you're not authenticated ")
            
            

