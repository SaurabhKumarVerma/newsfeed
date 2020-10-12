from django.shortcuts import render , get_object_or_404,redirect
from django.core.files.storage import FileSystemStorage 
from .models import Trending
from news.models import News
from cat.models import Cat
from subcat.models import SubCat


# Create your views here.

def trending_add(request):


	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")




	

	if request.method == "POST":

		trending = request.POST.get('trending')
		
		if trending == "":
			error = "All Fields Required"
			return render(request, 'back/error.html', {'error':error})


	

		b = Trending(txt = trending)
		b.save()

	return render(request, 'back/trending.html')


def trending_list(request):


	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")

	trending_lists = Trending.objects.all()

	return render(request , 'back/trending_list.html', {'trending_lists':trending_lists})

def trending_delete(request,pk):

	if not request.user.is_authenticated :

		return redirect("mylogin")

	b = Trending.objects.filter(pk=pk)
	b.delete()
	return redirect(trending_list)

def trending_edit(request,pk):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")

	mytxt =Trending.objects.get(pk=pk).txt 

	if request.method == "POST":


		txt = request.POST.get('txt')

		if txt == "":
			error = "All Fields Required"
			return render(request, 'back/error.html', {'error':error})


		b = Trending.objects.get(pk=pk)
		b.txt = txt
		b.save()

	return render(request, 'back/trending_edit.html', {'mytxt':mytxt,'pk':pk})

