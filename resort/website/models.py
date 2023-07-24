from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Resort(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to='resort_image')
    place=models.CharField(max_length=100)


class Customer(models.Model):
    Name=models.CharField(max_length=100)
    Address=models.CharField(max_length=100)
    Email=models.EmailField()
    Resort_name=models.CharField(max_length=100)
    Resort_price=models.IntegerField()
    Resort_place=models.CharField(max_length=100)
    CheckIn=models.DateField()
    CheckOut=models.DateField()
    Adults=models.IntegerField()
    Kids=models.IntegerField()

    

    
