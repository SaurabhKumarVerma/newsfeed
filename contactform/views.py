from django.shortcuts import render , get_object_or_404,redirect
from . models import ContactForm
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login , logout
import datetime


def contact_add(request): 	

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

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


	if request.method == "POST":

		name = request.POST.get('name')
		email = request.POST.get('email')
		txt = request.POST.get('msg')
		print(time)

		if name == "" or email == "" or txt == "" :
			msg = "All Feild Required"
			return render(request, 'fornt/msgbox.html', {'msg':msg} )

		b = ContactForm(name=name,email=email,txt=txt,date=today,time=time)
		b.save()
		msg = "Your Message Recevied"
		return render(request, 'front/msgbox.html', {'msg':msg} )

	return render(request, 'front/msgbox.html')

def contact_show(request):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")


	msg = ContactForm.objects.all()

	return render(request, 'back/contact_show.html' , {'msg':msg} )


def contact_delete(request, pk):


	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")


	b = ContactForm.objects.filter(pk=pk)
	b.delete()


	return redirect(contact_show)











