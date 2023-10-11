from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import hashvalue,partymembers,position,partyselection
import hashlib
from mine.models import track
from main.models import minerdb,votersdb,organizations
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.
def init(request):
    user=request.user
    a=organizations.objects.all()

    if request.method=='POST':
        c=request.POST.get('name')
        c=str(c)
        c=c.replace(' ','.').lower()
        url="http://"+c+".localhost:8000/voters/select/"
        return redirect(url)


    return render(request, "main.html",{'a':a})
@login_required(login_url='login')
def blockchain(request):
    print(11)
    k=partyselection.objects.last()
    user=request.user
    email=request.user.email
    vote=votersdb.objects.all()
    if k==None:
        print(111)
        return redirect("select")
    aa=partymembers.objects.filter(party_pos=k.pos)
    org_example=position.objects.last().org
    ll=organizations.objects.get(org=org_example)
    ll=ll.author

    if votersdb.objects.filter(mail=email,author=ll).exists():
        kk=votersdb.objects.get(mail=email,author=ll)
        mm=kk.pos
        for i in mm:
            print(settings.SESSION_COOKIE_AGE)
            if i==k.pos.participant:
                print(i)
                zz=mm.index(i)
                if kk.votepos[zz]==True:
                    print(1111)
                    return redirect('select')
                break

        data={'aa':aa,'user':user}
        if request.method=="POST":
            az=request.POST.get('vote')     
            prev=hashvalue.objects.last()
            if prev is None:
                a=""
            else:
                a=prev.hash_values 
            z="_"+az+"-"+a+"_"
            s=hashlib.sha256(z.encode()).hexdigest()
            prevvalue=hashvalue(hash_values=s)
            prevvalue.save()

            jj=minerdb.objects.filter(author=ll)
            for i in jj:
                i.voteval=False
                i.save()

            for i in mm:
                if i==k.pos.participant:
                    zz=mm.index(i)
                    kk.votepos[zz]=True
                    kk.save()

            k.delete()
            return redirect("results")
    else:
        return HttpResponse("Sorry you're not verified")           
    return render(request, "user.html",data)
@login_required(login_url='login')
def results(request):
    a=hashvalue.objects.last()
    b="Your Hash Value:"
    return render(request,"res.html",{'a':a,'b':b})
j=list()
@login_required(login_url='login')
def posselection(request):
    user=request.user
    group=user.groups.all()
    for i in group:
        if "voter" in str(i):
            settings.SESSION_COOKIE_AGE=180
            
    o=partyselection.objects.all()
    c=""
    if o is not None:
        o.delete()
    n=""
    email=request.user.email
    e=votersdb.objects.all()
    for i in e:
        if i.mail==email:
            c=position.objects.all()
            n=i.author
    data={'c':c}
    if request.method=='POST':
        g=request.POST.get('vote')
        if g is not None and g!='rog':
            m=minerdb.objects.all().filter(author=n)
            h=partyselection(pos=position.objects.get(participant=g))
            h.save() 
            for i in m:
                if i.voteval==False:
                    break
            else:
                return redirect('vote')    
    return render(request,"pos.html",data)

