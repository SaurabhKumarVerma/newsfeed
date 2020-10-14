from django.shortcuts import render , get_object_or_404,redirect
from django.core.files.storage import FileSystemStorage 
from . models import Main
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


# Create your views here.


def home(request):

	import json
	import requests
	


	url = 'https://api.ipdata.co?api-key=d9abf8a79adeeb7d86662dd39d1daa108d6a4b910a73abb1e3842efb'

	
	try:
		api = requests.get(url).json()
		
	except:
		api = "error"
	
	res = {key: api[key] for key in api.keys() & {'ip','city','latitude', 'longitude'}} 

	ip = res["ip"]
	
	city = res["city"]
	
	latitude = res["latitude"]
	

	longitude = res["longitude"]

	

	
	
	wheatherurl = "http://api.openweathermap.org/data/2.5/weather?lat="+ str(latitude) +"&lon="+ str(longitude) +"&appid=0148970bfb55217be51891fbd703aaff"

	try:
		wheatherapi = requests.get(wheatherurl).json()

		mitemp = wheatherapi['main']['temp_min']
		mxtemp = wheatherapi['main']['temp_max']
		min_temp = mitemp - 273.15
		max_temp = mxtemp - 273.15
		iconcode = wheatherapi['weather']['icon']
		
	except:
		api = "error"


	site = Main.objects.get(pk=1)
	news = News.objects.filter(act=1).order_by('-pk')
	cat =  Cat.objects.all()	
	subcat = SubCat.objects.all()
	lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
	
	popnews2 = News.objects.filter(act=1).order_by('-show')[:3]

	trending = Trending.objects.all().order_by('-pk')[:5]
	

	random_object = Trending.objects.all()[randint(0, len(trending) -1)]
	

	return render(request, 'front/home.html', {'site':site,'news':news, 'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2, 'trending':trending , 'wheatherapi':wheatherapi, 'min_temp':min_temp, 'max_temp':max_temp,'wheatherapi':wheatherapi})

def about(request):

	site = Main.objects.get(pk=1)
	news = News.objects.filter(act=1).order_by('-pk')
	cat =  Cat.objects.all()	
	subcat = SubCat.objects.all()
	lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
	popnews = News.objects.filter(act=1).order_by('-show')
	popnews2 = News.objects.filter(act=1).order_by('-show')[:3]

	return render(request, 'front/about.html', {'site':site,'news':news, 'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews':popnews,'popnews2':popnews2} )


def panel(request):

	if not request.user.is_authenticated :

		return redirect("mylogin")

	perm = 0
	perms = Permission.objects.filter(user=request.user)
	for i in perms:
		if i.codename=='master_user':perm = 1

	if perm == 0:
		error = '  '
		return render(request, 'back/error.html', {'error':error})

	rand = ""
	test = [ '~','@','#','$','%','^','&','*','(',')','_','-','+','=','|','<','>', ',','.','/','?','{','}','[',']',':',':',"'"]
	for i in range(100):
		rand = rand + random.choice(string.ascii_letters) + random.choice(test)



	return render(request, 'back/home.html', {'rand':rand})


def mylogin(request):

	if request.method == "POST":

		uusername = request.POST.get('username')
		upassword = request.POST.get('password')
		
		if uusername != "" and upassword != "":
			user = authenticate(username = uusername,password = upassword)
			
			if user != None:
				login(request,user)
				return redirect('panel')
		
	return render(request, 'front/login.html')

def register(request):

	if request.method == "POST":

		name = request.POST.get('name')
		uname = request.POST.get('uname')
		email = request.POST.get('email')
		regpassword = request.POST.get('regpassword')
		passwordverify = request.POST.get('passwordverify')

		if name == "":
			msg = "Name Feild Is Must"
			return render (request, 'front/msgbox.html',{'msg':msg})

		if regpassword != passwordverify:
			msg = "Password Is Not Mactching"
			return render(request, 'front/msgbox.html', {'msg':msg})

		SpecialSym = [ '~','@','#','$','%','^','&','*','(',')','_','-','+','=','|','<','>', ',','.','/','?','{','}','[',']',':',':',"'"]
		val = True
		


		if len(regpassword) < 8:
			error = "Password Must Be 8 Character"
			return render (request, 'back/error.html', {'error':error})

		if not any(char.isdigit() for char in regpassword):
			val = False
		if not any(char.isupper() for char in regpassword):
			val = False
		if not any(char.islower() for char in regpassword):
			val = False
		if not any(char in SpecialSym for char in regpassword):
			val = False

		if val == False:
			error = 'Password Must Contain Combination of Special Symbols'
			return render(request, 'back/error.html', {'error':error})
		
		if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0:
						
			ip, is_routable =  get_client_ip(request)
			if ip is None:
				ip = "0.0.0.0"
			else:
				if is_routable:
					ipv = "Public"
				else:
					ipv = "Private"
					
			print(ip,ipv)

			try:
				response = DbIpCity.get(ip,api_key='free')
				country = response.country + "|" + response.city
			except:
				country = 'Unknow'
				
		
			user = User.objects.create_user(username=uname,email=email,password=regpassword)
			b = Manager(name=name,utxt=uname,email=email,ip=ip, country=country)
			b.save()
			
			
		
		
			

	return render(request, 'front/login.html')

def mylogout(request):

	logout(request)

	return redirect('mylogin')

def site_setting(request):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})


	site = Main.objects.get(pk=1)

	if request.method == 'POST':

		name = request.POST.get('name')
		tell = request.POST.get('tell')
		fb = request.POST.get('fb')
		tw = request.POST.get('tw')
		yt = request.POST.get('yt')
		link = request.POST.get('link')
		txt = request.POST.get('txt')


		if fb == "":fb = "#"
		if tw == "":tw = "#"
		if yt == "":yt = "#"
		if link == "":link = "#"

		if name == "" or tell == "" or txt == "":
			error  = "These Feild Can not me Null"
			return render(request, 'back/error.html',{'error':error})


		try:

			myfile = request.FILES['file']
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			url = fs.url(filename)

			picurlbottom = url
			picbottom = filename

		except:
			picurlbottom = "-"
			picbottom = "-"

		try:
			myfile2 = request.FILES['file2']
			fs2 = FileSystemStorage()
			filename2 = fs2.save(myfile2.name, myfile2)
			url2 = fs2.url(filename2)

			picurltop = url2
			pictop = filename2
			
		except:

			picurltop = "-"
			pictop = "-"

		b = Main.objects.get(pk=1)
		b.name = name
		b.tell = tell
		b.fb = fb
		b.tw = tw
		b.yt = yt
		b.link = link
		b.about = txt
		if picurlbottom != "-":b.picurlbottom = picurlbottom
		if picbottom != "-":b.picbottom = picbottom

		if picurltop != "-":b.picurltop = picurltop
		if pictop != "-":b.pictop = pictop

		b.save()

	return render(request , 'back/setting.html',{'site':site})

def about_setting(request):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})


	if not request.user.is_authenticated :

		return redirect("mylogin")

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if request.method == "POST":

		txt = request.POST.get('txt')

		if txt == "":
			error = "Feild Can not Be Empty"
			return render(request, 'back/error.html',{'error':error})
		b = Main.objects.get(pk=1)
		b.abouttxt = txt
		b.save()


	about = Main.objects.get(pk=1).abouttxt


	return render(request, 'back/about_setting.html' , {'about':about})


def contact(request):


	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	site = Main.objects.get(pk=1)
	news = News.objects.all().order_by('-pk')
	cat =  Cat.objects.all()	
	subcat = SubCat.objects.all()
	lastnews = News.objects.all().order_by('-pk')[:3]
	popnews = News.objects.all().order_by('-show')
	popnews2 = News.objects.all().order_by('-show')[:3]

	return render(request, 'front/contact.html', {'site':site,'news':news, 'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews':popnews,'popnews2':popnews2})


def change_pass(request):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")

	if request.method == "POST":

		oldpass = request.POST.get('oldpassword')
		newpass = request.POST.get('newpassword')

		# en_pass = pbkdf2_sha256.encrypt(newpass, round=12000, salt_size=32)

		if oldpass == "" or newpass == "":
			error = "All Fields Required"
			return render(request, 'back/error.html', {'error':error})

		user = authenticate(username=request.user, password=oldpass)

		SpecialSym = [ '~','@','#','$','%','^','&','*','(',')','_','-','+','=','|','<','>', ',','.','/','?','{','}','[',']',':',':',"'"]
		val = True
		if user != None:

			if len(newpass) < 8:
				error = "Password Must Be 8 Character"
				return render (request, 'back/error.html', {'error':error})

			if not any(char.isdigit() for char in newpass):
				val = False
			if not any(char.isupper() for char in newpass):
				val = False
			if not any(char.islower() for char in newpass):
				val = False
			if not any(char in SpecialSym for char in newpass):
				val = False

			if val == True:
				
				user = User.objects.get(username=request.user)
				user.set_password(newpass)
				user.save()
				return redirect('mylogout')
				
			else:
				error = 'Password Must Contain Combination of Special Symbols'
				return render(request, 'back/error.html', {'error':error})
				
	
		else:
			error = "Your Password Is Not Correct"
			return render(request, 'back/error.html',{'error':error})

	return render(request, 'back/change_pass.html')