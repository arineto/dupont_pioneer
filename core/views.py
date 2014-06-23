from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from random import randint
from core.forms import *
from core.models import *


FILTER_VALUES = {
	"Canola (Roundup Ready)":"canola_roundup",
	"Canola (LL)":"canola_ll",
	"Canola (CL)":"canola_cl",
	"Canola (Speciality)":"canola_speciality",
	"Corn":"corn",
	"Soybean":"soybean",
}


def home(request, filter_value=None):
	if not request.user.is_authenticated():
		return redirect('/login/')

	polygons = Polygon.objects.all()
	
	if filter_value is not None:
		polygons = filter_farms(filter_value)

	try:
		if request.session['error']:
			error = request.session['error']
			del request.session['error']
		else:
			error = ""
	except:
		error = ""
	products = Product.objects.all()
	return render(request, 'home.html', {'polygons':polygons, 'filters':products, 'error':error})



def filter_farms(filter_value):
	farms = []
	filter_value = FILTER_VALUES[filter_value]
	for farm in Farm.objects.all():
		if filter_value == "canola_roundup":
			if farm.canola_roundup > 0:
				farms += [farm]
		elif filter_value == "canola_ll":
			if farm.canola_ll > 0:
				farms += [farm]
		elif filter_value == "canola_cl":
			if farm.canola_cl > 0:
				farms += [farm]
		elif filter_value == "canola_speciality":
			if farm.canola_speciality > 0:
				farms += [farm]
		elif filter_value == "corn":
			if farm.corn > 0:
				farms += [farm]
		elif filter_value == "soybean":
			if farm.soybean > 0:
				farms += [farm]
	polygons = []
	for polygon in Polygon.objects.all():
		if polygon.farm_info in farms:
			polygons += [polygon]
	return polygons


@login_required
def save_map(request, map_id=None):
	if not request.user.is_superuser:
		return redirect('/')

	if request.method == 'POST':
		if map_id:
			instance = Polygon.objects.get(id=map_id)
			form = PolygonEditForm(request.POST, instance=instance)
		else:
			form = PolygonForm(request.POST)

		if form.is_valid():
			form.save()
		else:
			request.session['error'] = "Fill every field"

	return redirect('/')


@login_required
def delete_map(request, map_id):
	if not request.user.is_superuser:
		return redirect('/')

	Polygon.objects.get(id=map_id).delete()
	return redirect('/')


@login_required
def edit_map(request, map_id):
	if not request.user.is_superuser:
		return redirect('/')

	polygons = Polygon.objects.all()
	polygon = Polygon.objects.get(id=map_id)
	products = Product.objects.all()
	return render(request, 'home.html', {'polygons':polygons, 'filters':products, 'edit':map_id, 'polygon':polygon})


@login_required
def add_info(request, map_id):
	if not request.user.is_superuser:
		return redirect('/')

	polygons = Polygon.objects.all()
	polygon = Polygon.objects.get(id=map_id)
	products = Product.objects.all()

	if request.method == 'POST':
		form = FarmForm(request.POST)
		if form.is_valid():
			farm = form.save()
			polygon.farm_info = farm
			polygon.save()
			return redirect('/')
	else:
		form = FarmForm()

	return render(request, 'home.html', {'polygons':polygons, 'filters':products, 'add_info':map_id, 'polygon':polygon, 'form':form})


@login_required
def edit_info(request, farm_id):
	if not request.user.is_superuser:
		return redirect('/')

	instance = Farm.objects.get(id=farm_id)
	if request.method == 'POST':
		form = FarmForm(request.POST, instance=instance)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = FarmForm(instance=instance)

	polygons = Polygon.objects.all()
	polygon = Polygon.objects.get(farm_info=instance)
	products = Product.objects.all()
	return render(request, 'home.html', {'polygons':polygons, 'filters':products, 'edit_info':polygon.id, 'polygon':polygon, 'form':form})


@login_required
def remove_info(request, farm_id):
	if not request.user.is_superuser:
		return redirect('/')
	Farm.objects.get(id=farm_id).delete()
	return redirect('/')


def login_aux(request):
	error = None
	if request.method == "POST":
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	      if user.is_active:
	        login(request, user)
	        AccessInfo.objects.create(user=user)
	        return redirect('/')
	      else:
	      	error = "Not active user"
	    else:
	    	error = "Invalid username/password"

	return render(request, 'login.html', {'error':error})


def logout_aux(request):
	logout(request)
	return redirect('/')


@login_required
def access_info(request, username=None):
	if not request.user.is_superuser:
		return redirect('/')

	if username:
		info = AccessInfo.objects.filter(user=User.objects.get(username=username)).order_by('-date')
	else:
		info = AccessInfo.objects.all().order_by('-date')

	users = User.objects.all()
	return render(request, 'access_info.html', {'access_info':True,'info':info, 'users':users})


def forgot_password(request):
	answer = None
	if request.method == "POST":
		email = request.POST.get("email")
		try:
			user = User.objects.get(email=email)
			new_password = randint(100000, 999999)
			message = "Hello, \nThis is an answer to password recovery. Please change your password for security reasons.\nNew Password: "+str(new_password)
			email = EmailMessage('DuPont Pioneer', message, to=[email])
			email.send()
			user.set_password(new_password)
			user.save()
			answer = "The password was sent to you email."
		except:
			answer = "There are no accounts registered in this email."

	return render(request, 'login.html', {'forgot_password':True, 'answer':answer})


@login_required
def change_password(request):
	error = None
	polygons = Polygon.objects.all()
	products = Product.objects.all()
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if not request.user.check_password(request.POST.get('old_password')):
			error = "Wrong old password"
		else:
			if form.is_valid():
				request.user.set_password(request.POST.get('password1'))
				request.user.save()
				return redirect('/')
	else:
		form = ChangePasswordForm()
	return render(request, 'home.html', {'polygons':polygons, 'filters':products, 'change_password':True, 'form':form, 'error':error})




