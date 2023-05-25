from django.db import models

# Create your models here.

class login(models.Model):
    username=models.CharField(max_length=90, unique=True)
    password = models.CharField(max_length=90)
    type = models.CharField(max_length=90)

class user(models.Model):
    lid = models.ForeignKey(login,on_delete=models.CASCADE)
    fname = models.CharField(max_length=90)
    lname = models.CharField(max_length=90)
    gender = models.CharField(max_length=90)
    age = models.IntegerField()
    phone = models.BigIntegerField()
    place = models.CharField(max_length=150)
    post = models.CharField(max_length=90)
    pin = models.IntegerField()
    email = models.EmailField()

class artist(models.Model):
    lid = models.ForeignKey(login, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    gender = models.CharField(max_length=90)
    age = models.IntegerField()
    phone = models.BigIntegerField()
    address = models.TextField()
    work_experience = models.IntegerField()
    joining_date = models.DateField()

class artwork(models.Model):
    aid = models.ForeignKey(artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    price = models.IntegerField()
    availability = models.CharField(max_length=90)
    image = models.FileField()
    description = models.TextField()
    date_created = models.DateField()

class artworkOrder(models.Model):
    uid = models.ForeignKey(user, on_delete=models.CASCADE)
    awid = models.ForeignKey(artwork, on_delete=models.CASCADE)
    date = models.DateField()
    staus = models.CharField(max_length=90)

class customerArtworkReq(models.Model):
    uid = models.ForeignKey(user, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    description = models.TextField()
    staus = models.CharField(max_length=90)

class artworkSellReq(models.Model):
    awid = models.ForeignKey(artwork, on_delete=models.CASCADE)
    aid = models.ForeignKey(artist, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=90)