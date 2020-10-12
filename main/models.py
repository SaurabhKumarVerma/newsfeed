from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Main(models.Model):

	name = models.CharField(max_length = 50)
	about = models.TextField()
	abouttxt = models.TextField(default="")
	fb = models.CharField(max_length = 50)
	tw = models.CharField(max_length = 50)
	yt = models.CharField(max_length = 50)
	tell = models.CharField(max_length = 50)
	link  = models.CharField(max_length = 50)
	set_name = models.CharField(max_length = 50)
	picurlbottom = models.TextField(default='-')
	picbottom = models.TextField(default='-')
	picurltop = models.TextField(default='-')
	pictop = models.TextField(default='-')


	def __str__(self):
		return self.set_name + " | " + str(self.pk) 

	