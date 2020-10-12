from django.shortcuts import render , get_object_or_404,redirect
from . models import Cat
from manager.models import Manager
# Create your views here.

def cat_list(request):


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
	
	cat = Cat.objects.all()
	return render(request, 'back/cat_list.html', {'cat':cat})

def cat_add(request):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	
	if not request.user.is_authenticated :

		return redirect("mylogin")

	
	if request.method == "POST":

		name = request.POST.get('categorytitle')

		
		if name == "":

			error = "Feild Can Not Be empty"
			return render(request, 'back/error.html', {'error':error})

		if len(Cat.objects.filter(name=name)) != 0:

			error = "Name Already Be Taken"
			return render(request, 'back/error.html', {'error':error})

		b = Cat(name = name)
		b.save()
		return redirect("cat_list")
			
		
			
		
		
	return render(request, 'back/cat_add.html')

def cat_delete(request,pk):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	
	if not request.user.is_authenticated :

		return redirect("mylogin")



	try:

		b = Cat.objects.get(pk=pk)
		b.delete()
	except Exception as e:
		error = print(e)
		return render(request, 'back/error.html', {'error':error})


	return redirect('cat_list')