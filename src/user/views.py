from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import hashvalue,partymembers,position,partyselection
import hashlib
from mine.models import track
from main.models import minerdb,votersdb,organizations
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User,Group
from exp.decor import convertor
from django.contrib.auth import logout
# Create your views here.
def init(request):
    user=request.user
    org=organizations.objects.all()

    if request.method=='POST':
        org_req=request.POST.get('name')
        org_req=convertor(org_req)
        url="http://"+org_req+".localhost:8000/voters/select/"
        return redirect(url)

    return render(request, "main.html",{'org':org})

@login_required(login_url='login')
def blockchain(request):

    party_sel=partyselection.objects.last()
    user=request.user
    email=user.email
    vote=votersdb.objects.all()

    if party_sel==None:
        return redirect("select")
    party_mem=partymembers.objects.filter(party_pos=party_sel.pos)
    org_example=position.objects.last().org

    if votersdb.objects.filter(mail=email,org=org_example).exists():
        voters_db=votersdb.objects.get(mail=email)
        vote_pos=voters_db.pos
        for i in vote_pos:
            if i==party_sel.pos.participant:
                ind=vote_pos.index(i)
                if voters_db.votepos[ind]==True:
                    return redirect('select')
                break

        data={'party_mem':party_mem,'user':user}
        if request.method=="POST":
            vote=request.POST.get('vote')     
            prev=hashvalue.objects.last()
            if prev is None:
                prev=""
            else:
                prev=prev.hash_values 
            b_hash="_"+vote+"-"+prev+"_"
            a_hash=hashlib.sha256(b_hash.encode()).hexdigest()
            hashed=hashvalue(hash_values=a_hash)
            hashed.save()

            miner_db=minerdb.objects.filter(org=org_example)
            for i in miner_db:
                i.voteval=False
                i.save()

            for i in vote_pos:
                if i==party_sel.pos.participant:
                    ind=vote_pos.index(i)
                    voters_db.votepos[ind]=True
                    voters_db.save()

            party_sel.delete()
            return redirect("results")
    else:
        return HttpResponse("Sorry you're not verified")           
    return render(request, "user.html",data)

@login_required(login_url='login')
def results(request):
    a=hashvalue.objects.last()
    b="Your Hash Value:"
    return render(request,"res.html",{'a':a,'b':b})

@login_required(login_url='login')
def posselection(request):
    http=str(request.build_absolute_uri())
    http=http.removeprefix("http://")
    http,a=http.split(".localhost")
    user=request.user
    user_email=user.email
    parties,types="",""

    if user.groups.filter(name='voter-'+http).exists():
        types="voter"
        settings.SESSION_COOKIE_AGE=180     
    elif user.groups.filter(name='creator-'+http).exists():
        parties=position.objects.all()
        types="creator"
    else:
        return redirect('logout')

    if partyselection.objects.all().exists():
        selection=partyselection.objects.all()
        selection.delete()
    org_example=position.objects.last().org
    if user.groups.filter(name='voter-'+http).exists():
        parties=votersdb.objects.get(mail=user_email,org=org_example).pos
    
    data={'parties':parties,'types':types}
    
    if request.method=='POST':
        select=request.POST.get('vote')
        if select is not None and select!='rog':
            miner_db=minerdb.objects.filter(org=org_example)
            party_sel=partyselection(pos=position.objects.get(participant=select))
            party_sel.save() 
            for i in miner_db:
                if i.voteval==False:
                    break
            else:
                return redirect('vote')    
    return render(request,"pos.html",data)

