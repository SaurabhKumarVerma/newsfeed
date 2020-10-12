from django.shortcuts import render , get_object_or_404,redirect
from django.core.files.storage import FileSystemStorage 
from . models import Newsletter
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from trending.models import Trending
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User, Group, Permission
import random
from random import randint
from passlib.hash import pbkdf2_sha256
from django.contrib.auth.hashers import make_password, check_password
from manager.models import Manager


def news_letter(request):

    if request.method == 'POST':
        txt = request.POST.get('name')

        b = Newsletter(txt=txt,status=1)
        b.save()

    return redirect('home')


def news_email(request):

    perm = 0
    for i in request.user.groups.all():
        if i.name == 'mastername' :perm = 1

    if not request.user.is_authenticated:
        return redirect("mylogin")


    email = Newsletter.objects.filter(status=1)

    return render(request, 'back/email.html',{'email':email})

def news_phone(request):

    perm = 0
    for i in request.user.groups.all():
        if i.name == 'mastername' :perm = 1

    if not request.user.is_authenticated:
        return redirect("mylogin")


    phone = Newsletter.objects.filter(status=0)

    return render(request, 'back/phone.html',{'phone':phone})