from django.shortcuts import render , get_object_or_404,redirect
from . models import Cat
from manager.models import Manager
import csv
from django.http import HttpResponse
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

def export_csv_data(request):

	response  = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="cat.csv"'

	writer = csv.writer(response)
	writer.writerow(['Cartegory','Counter'])

	for i in Cat.objects.all():
		writer.writerow([i.name, i.count])

	return response

def import_csv_data(request):

	if request.method == "POST":

		csv_file = request.FILES['csv_file']

		if not csv_file.name.endswith('.csv'):
			error = "Please Upload CSV File"
			return render(request, 'back/error.html', {'error':error})
		
		if csv_file.multiple_chunks():
			error = "File Size is Too Large"
			return render(request, 'back/error.html', {'error':error})


		file_data = csv_file.read().decode("utf-8")

		lines = file_data.split("\n")

		for line in lines:
			feilds = line.split(",")

			try:
				if len(Cat.objects.filter(name=feilds[0])) == 0 and feilds[0] != "Title" and feilds[0] != "":
					b = Cat(name=feilds[0])
					b.save()
				
			except:
				print('Finshed')


	return redirect('cat_list')