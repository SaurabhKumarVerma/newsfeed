from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Blacklist(models.Model):

	ip = models.CharField(max_length = 20)
	
	
	def __str__(self):
		return self.ip
