from django.shortcuts import render , get_object_or_404,redirect
from django.core.files.storage import FileSystemStorage 
from . models import Comment
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from trending.models import Trending
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User, Group, Permission
import random
import string
import datetime
from random import randint
from passlib.hash import pbkdf2_sha256
from django.contrib.auth.hashers import make_password, check_password
from manager.models import Manager


def news_cm_add(request,pk):


    if request.method == 'POST':

        now = datetime.datetime.now()
        
        year = now.year
        month = now.month
        day = now.day
        

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)

        today = (str(year) +"/"+ str(month) +"/"+ str(day))	
        time = str(now.hour) + ":"+ str(now.minute)

        cm = request.POST.get('msg')
        

        if request.user.is_authenticated:

            manager = Manager.objects.get(utxt=request.user)
            b = Comment(name=manager.name,email=manager.email,cm=cm,news_id=pk,date=today,time=time)
            b.save()
        else:
            
            msg = request.POST.get('msg')
            name = request.POST.get('name')
            email = request.POST.get('email')

            a = Comment(name=name,email=email,cm=msg,news_id=pk,date=today,time=time)
            a.save()

    newsname = News.objects.get(pk=pk).name
    print(newsname)


    return redirect('news_detail',word=newsname)


def comment_list(request):

    if not request.user.is_authenticated :

        return redirect("mylogin")

    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser' : perm = 1

    if perm == 0:
        error = 'URL NOT FOUND'
        return render(request , 'back/error.html', {'error':error})

    


    comment = Comment.objects.all()

    return render(request, 'back/comment_list.html', {'comment':comment})


def comment_del(request, pk):

    if not request.user.is_authenticated :

        return redirect("mylogin")

    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser' : perm = 1

    if perm == 0:
        error = 'URL NOT FOUND'
        return render(request , 'back/error.html', {'error':error})

    


    comment = Comment.objects.filter(pk=pk)
    comment.delete()

    return redirect('comment_list')

def comment_confirm(request, pk):

    if not request.user.is_authenticated :

        return redirect("mylogin")

    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser' : perm = 1

    if perm == 0:
        error = 'URL NOT FOUND'
        return render(request , 'back/error.html', {'error':error})

    


    comment = Comment.objects.get(pk=pk)
    comment.status = 1
    comment.save()

    return redirect('comment_list')