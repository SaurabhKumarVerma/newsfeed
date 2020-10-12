from django.shortcuts import render , get_object_or_404,redirect
from . models import SubCat
from cat.models import Cat
# Create your views here.

def subcat_list(request):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")
	
	subcat = SubCat.objects.all()
	return render(request, 'back/subcat_list.html', {'subcat':subcat})

def subcat_add(request):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")

	cat = Cat.objects.all()

	if request.method == "POST":

		name = request.POST.get('subcategorytitle')
		catid = request.POST.get('subcat')

		
		if name == "":

			error = "Feild Can Not Be empty"
			return render(request, 'back/error.html', {'error':error})

		if len(SubCat.objects.filter(name=name)) != 0:

			error = "Name Already Be Taken"
			return render(request, 'back/error.html', {'error':error})

		catname = Cat.objects.get(pk=catid).name
		b = SubCat(name = name, catname = catname, catid = catid)
		b.save()
		return redirect("subcat_list")
			
		
			
		
		
	return render(request, 'back/subcat_add.html', {'cat':cat})

def subcat_delete(request,pk):

	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser' : perm =1

	if perm == 0:
		error = 'URL Not Found'
		return render(request, 'back/error.html', {'error':error})

	if not request.user.is_authenticated :

		return redirect("mylogin")

	try:

		b = SubCat.objects.get(pk=pk)
		b.delete()
	except:
		error = "Something Went Wrong"
		return render(request, 'back/error.html', {'error':error})


	return redirect('subcat_list')