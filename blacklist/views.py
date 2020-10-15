from django.shortcuts import render , get_object_or_404,redirect
from django.core.files.storage import FileSystemStorage 
from . models import Blacklist
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from trending.models import Trending
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User, Group, Permission
import random
import string
from random import randint
from passlib.hash import pbkdf2_sha256
from django.contrib.auth.hashers import make_password, check_password
from manager.models import Manager
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity




def black_list(request):

    ip = Blacklist.objects.all()

    username = []
    ip = []
    for i in  Manager.objects.all():
       if i.ip != ip:
           username.append(i)
           ip.append(i)

    print(username)

    

    return render(request,'back/backlist.html' , {'ip':ip,'username':username})


def ip_add(request):


    if request.method == 'POST':

        ip = request.POST.get('ip')

        if ip != "":
            b = Blacklist(ip=ip)
            b.save()

    return redirect('black_list')


def ip_del(request,pk):

    #Need TO work on susupend to specifig ip

    b = Blacklist.objects.filter(pk=pk)
    b.delete()
    
    return redirect('black_list')


