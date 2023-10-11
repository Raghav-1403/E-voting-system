from django.shortcuts import render,HttpResponse
from user.models import partymembers,hashvalue
from .models import count,track
from main.models import minerdb
from django.contrib.auth.models import User
import hashlib
# Create your views here.
def mining(request):
    email=request.user.email
    choice=minerdb.objects.all()
    data={}
    select=""
    if minerdb.objects.filter(mail=email).exists():
        select=minerdb.objects.get(mail=email)
    else:
        return HttpResponse("sorry you're not authenticated ")
    g=hashvalue.objects.last()
    first=hashvalue.objects.first()
    data={'g':g}
    j=track.objects.last()
    k=""
    l=g.id
    if j is not None:
        k=j.trace 
        v=hashvalue.objects.get(id=k)
        b=v.hash_values
    else:
        k=0
        b=""
    
    if request.method=='POST':
        if k!=l:
            c=partymembers.objects.all()
            e=g.hash_values
            for j in c:
                d=j.party
                z="_"+d+"-"+b+"_"
                x=hashlib.sha256(z.encode()).hexdigest()
                if e==x:
                    m=count(cou=d)
                    m.save()    
            h=track(trace=l)
            h.save()
        select.voteval=True
        select.save()
        s=count.objects.last()
        data={'s':s,'g':g}
    return render(request,"miner.html",data)
def results(request):
    a=count.objects.all()
    return render(request,'result')
            
            

