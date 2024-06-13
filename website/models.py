from django.db import models
from website.validators import validate_custom_email


class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100,unique=True, validators=[validate_custom_email])
	phone = models.CharField(max_length=16, blank=True, null=True)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")
