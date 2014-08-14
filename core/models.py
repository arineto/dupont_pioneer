from django.db import models
from django.contrib.auth.models import User


class Polygon(models.Model):
	points = models.CharField(max_length=100000)
	title = models.CharField(max_length=100)
	color = models.CharField(max_length=7)
	farm_info = models.ForeignKey('Farm', null=True, blank=True, on_delete=models.SET_NULL)
	date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title


class Farm(models.Model):
	address = models.CharField(max_length=100, verbose_name="Address")
	phone = models.CharField(max_length=15, verbose_name="Phone")
	sales_representative = models.CharField(max_length=100, verbose_name="Sales Representative")
	email = models.EmailField(verbose_name="Email")
	decision_maker = models.CharField(max_length=100, verbose_name="Decision Maker")
	canola_roundup = models.IntegerField(verbose_name="Canola Roundup Ready")
	canola_ll = models.IntegerField(verbose_name="Canola (LL)")
	canola_cl = models.IntegerField(verbose_name="Canola (CL)")
	canola_speciality = models.IntegerField(verbose_name="Canola (Speciality)")
	corn = models.IntegerField(verbose_name="Corn")
	soybean = models.IntegerField(verbose_name="Soybean")



class AccessInfo(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.user.username


class Product(models.Model):
	name = models.CharField(max_length=50, verbose_name="Name")
	icon = models.FileField(upload_to="icons/", verbose_name="Icon")

	def __unicode__(self):
		return self.name


class LoginPicture(models.Model):
	picture = models.FileField(upload_to="login_pictures/")