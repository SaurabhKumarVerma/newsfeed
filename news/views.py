from django.shortcuts import render , get_object_or_404,redirect
from . models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage 
import datetime
from subcat.models import SubCat
from cat.models import Cat
from comment.models import Comment
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
import qrcode
# Create your views here.

def news_detail(request,word):

	

	site = Main.objects.get(pk=1)
	news = News.objects.all().order_by('-pk')
	cat =  Cat.objects.all()	
	subcat = SubCat.objects.all()
	lastnews = News.objects.all().order_by('-pk')[:3]

	shownews = News.objects.filter(name=word)
	popnews = News.objects.all().order_by('-show')
	popnews2 = News.objects.all().order_by('-show')[:3]

	tagname = News.objects.get(name=word).tag
	tag = tagname.split(',')

	try:
		mynews = News.objects.get(name=word)
		mynews.show = mynews.show + 1
		mynews.save()
	except:
		print("Can't Add Show " )

	code = News.objects.get(name=word).pk
	comment = Comment.objects.filter(news_id=code ,status = 1).order_by('-pk')
	cmcount = len(comment)

	link = "/urls/" + str(News.objects.get(name=word).rand)
	qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4,)
	qr.add_data('link')
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	

	return render(request, 'front/news_detail.html',{'img':img,'link':link,'cmcount':cmcount,'comment':comment,'code':code,'site':site,'news':news, 'cat':cat,'subcat':subcat,'lastnews':lastnews,'shownews':shownews,'popnews2':popnews2,'tag':tag,'popnews':popnews})


def news_detail_short(request,pk):

	

	site = Main.objects.get(pk=1)
	news = News.objects.all().order_by('-pk')
	cat =  Cat.objects.all()	
	subcat = SubCat.objects.all()
	lastnews = News.objects.all().order_by('-pk')[:3]

	shownews = News.objects.filter(rand=pk)
	popnews = News.objects.all().order_by('-show')
	popnews2 = News.objects.all().order_by('-show')[:3]

	tagname = News.objects.get(rand=pk).tag
	tag = tagname.split(',')

	try:
		mynews = News.objects.get(rand=pk)
		mynews.show = mynews.show + 1
		mynews.save()
	except:
		print("Can't Add Show " )
	return render(request, 'front/news_detail.html',{'site':site,'news':news, 'cat':cat,'subcat':subcat,'lastnews':lastnews,'shownews':shownews,'popnews2':popnews2,'tag':tag,'popnews':popnews})





def news_list(request):

	if not request.user.is_authenticated :

		return redirect("mylogin")

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0 :
		news = News.objects.filter(writer=request.user)
	elif perm == 1:
		newss = News.objects.all()
		paginator = Paginator(newss,2)
		page = request.GET.get('page')

		try:
			news = paginator.page(page)
		except EmptyPage :
			news = paginator.page(paginator.num_page)
		except PageNotAnInteger :
			news = paginator.page(1)
	
	
	return render(request, 'back/news_list.html',{'news':news})

def news_add(request):

	if not request.user.is_authenticated :

		return redirect("mylogin")

	
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

	date = str(year) + str(month) + str(day)
	randint = str(random.randint(1000,9999))
	rand = date + randint
	rand = int(rand)
	print(rand)
	
	while len(News.objects.filter(rand=rand)) != 0:
		randint = str(random.randinit(1000,9999))
		rand = date + randint
		rand = int(rand)

	
	cat = SubCat.objects.all()

	
	if request.method == "POST":

		newstitle = request.POST.get('newstitle')
		newscat = request.POST.get('newscat')
		newstxtshort = request.POST.get('newstxtshort')
		newstxt = request.POST.get('newstxt')
		newsid = request.POST.get('newscat')
		tag = request.POST.get('tag')

		if newstitle == "" or newstxtshort == "" or newstxt == "" or newscat == "":
			error  = "All Feilds Are Required"
			return render(request, 'back/error.html',{'error':error})
		try:
			myfile = request.FILES['file']
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			url = fs.url(filename)

			if str(myfile.content_type).startswith("image"):

				if myfile.size < 5000000:


					newsname = SubCat.objects.get(pk=newsid).name
					ocatid = SubCat.objects.get(pk=newsid).catid


					b = News(name = newstitle ,short_txt = newstxtshort, body_txt = newstxt , date = today, pic = filename,picurl = url, writer = request.user, catname = newsname, catid = newsid, show = 0 ,time = time, ocatid = ocatid,tag=tag, rand=rand )

					b.save()

					count = len(News.objects.filter(ocatid = ocatid))

					b = Cat.objects.get(pk=ocatid)
					b.count = count
					b.save()
					return redirect("news_list")
				else:
					fs = FileSystemStorage()
					fs.delete(filename)
					error = "Image Bigger Than 5 MB"
					return render(request, 'back/error.html', {'error':error})
			else:

				fs = FileSystemStorage()
				fs.delete(filename)
				error = "Image not Supported"
				return render(request, 'back/error.html', {'error':error})

		except:
			error = "Went  Something Wrong"
			return render(request, 'back/error.html', {'error':error})
	return render(request, 'back/news_add.html',{'cat':cat})


def news_delete(request,pk):


	if not request.user.is_authenticated :

		return redirect("mylogin")


	
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0 :
		a = News.objects.get(pk=pk).writer
		if str(a) != str(request.user):
			error = 'Invalid User'
			return render(request, 'back/error.html',{'error':error})


	try:

		b = News.objects.get(pk=pk)
		fs = FileSystemStorage()
		fs.delete(b.pic)

		ocatid = News.objects.get(pk=pk).ocatid

		b.delete()

		count = len(News.objects.filter(ocatid=ocatid))

		m = Cat.objects.get(pk=ocatid)
		m.count = count
		m.save()
	except:

		error = "Something Wrong"
		return render(request, 'back/error.html', {'error':error})

	return redirect("news_list")


def news_edit(request,pk):


	if not request.user.is_authenticated :

		return redirect("mylogin")

	
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0 :
		a = News.objects.get(pk=pk).writer
		if str(a) != str(request.user):
			error = 'Invalid User'
			return render(request, 'back/error.html',{'error':error})

	if len(News.objects.filter(pk=pk)) == 0:

		error = "News Not Found "
		return render(request, 'back/error.html', {'error':error})


	news = News.objects.get(pk=pk)
	cat = SubCat.objects.all()

	if request.method == "POST":

		newstitle = request.POST.get('newstitle')
		newscat = request.POST.get('newscat')
		newstxtshort = request.POST.get('newstxtshort')
		newstxt = request.POST.get('newstxt')
		newsid = request.POST.get('newscat')
		tag = request.POST.get('tag')

		if newstitle == "" or newstxtshort == "" or newstxt == "" or newscat == "":
			error  = "All Feilds Are Required"
			return render(request, 'back/error.html',{'error':error})
			
		try:
			myfile = request.FILES['file']
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			url = fs.url(filename)

			if str(myfile.content_type).startswith("image"):

				if myfile.size < 5000000:


					newsname = SubCat.objects.get(pk=newsid).name

					b = News.objects.get(pk=pk)

					fss = FileSystemStorage()
					fss.delete(b.pic)	
					
					b.name = newstitle
					b.short_txt = newstxtshort
					b.body_txt = newstxt
					b.pic =  filename
					b.picurl = url
					b.catname = newsname
					b.catid = newsid
					b.tag = tag
					b.act = 0
					b.save()
					return redirect("news_list")
				else:
					fs = FileSystemStorage()
					fs.delete(filename)
					error = "Image Bigger Than 5 MB"
					return render(request, 'back/error.html', {'error':error})
			else:

				fs = FileSystemStorage()
				fs.delete(filename)
				error = "Image not Supported"
				return render(request, 'back/error.html', {'error':error})

		except:

			newsname = SubCat.objects.get(pk=newsid).name

			

			b = News.objects.get(pk=pk)

			b.name = newstitle
			b.short_txt = newstxtshort
			b.body_txt = newstxt
			b.catname = newsname
			b.catid = newsid
			b.tag = tag
			b.save()
			return redirect("news_list")

	return render(request, 'back/news_edit.html',{'pk':pk, 'news':news, 'cat':cat})


def news_publish(request,pk):


	if not request.user.is_authenticated :

		return redirect("mylogin")

	news = News.objects.get(pk=pk)
	news.act = 1
	news.save()

	return redirect("news_list")


def news_suspend(request,pk):


	if not request.user.is_authenticated :

		return redirect("mylogin")

	news = News.objects.get(pk=pk)
	news.act = 0
	news.save()

	return redirect("news_list")

def all_news(request,word):

	catid = Cat.objects.get(name=word).pk
	print(catid)
	allnews = News.objects.filter(ocatid=catid)

	site = Main.objects.get(pk=1)
	news = News.objects.filter(act=1).order_by('-pk')
	cat =  Cat.objects.all()	
	subcat = SubCat.objects.all()
	lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
	popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
	lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]
	

	return render(request, 'front/all_news.html',{'catid':catid,'all_news':all_news,'lastnews2':lastnews2,'site':site,'news':news, 'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2})

