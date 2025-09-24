from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    place=models.CharField(max_length=100)
    pincode=models.BigIntegerField()
    district=models.CharField(max_length=100)
    photo=models.FileField()
    latitude=models.FloatField()
    longitude=models.FloatField()

class category_table(models.Model):
    category=models.CharField(max_length=100)

class Book_table(models.Model):
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    photo = models.FileField()
    details = models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    rent_price=models.CharField(max_length=100)
    CATEGORY=models.ForeignKey(category_table,on_delete=models.CASCADE)

class request_table(models.Model):
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    BOOK = models.ForeignKey(Book_table, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    date = models.DateField()

class rent_table(models.Model):
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    BOOK = models.ForeignKey(Book_table, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    date = models.DateField()

class payment_table(models.Model):
    REQUEST=models.ForeignKey(request_table,on_delete=models.CASCADE)
    amount=models.BigIntegerField()
    status = models.CharField(max_length=100)
    date = models.DateField()

class rent_payment_table(models.Model):
    RENT=models.ForeignKey(rent_table,on_delete=models.CASCADE)
    amount=models.BigIntegerField()
    status = models.CharField(max_length=100)
    date = models.DateField()

class review_table(models.Model):
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    BOOK = models.ForeignKey(Book_table, on_delete=models.CASCADE)
    review = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    date = models.DateField()

class notification_table(models.Model):
    notification=models.CharField(max_length=100)
    date = models.DateField()
    RENT = models.ForeignKey(rent_table, on_delete=models.CASCADE)
    USER = models.ForeignKey(User_table, on_delete=models.CASCADE)


class Complaint_table(models.Model):
    USER=models.ForeignKey(User_table,on_delete=models.CASCADE)
    date=models.DateField()
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)

class chat_table(models.Model):
    FROMID=models.ForeignKey(User, on_delete=models.CASCADE,related_name='fuser')
    TOID=models.ForeignKey(User, on_delete=models.CASCADE,related_name='tuser')
    message=models.CharField(max_length=100)
    date = models.DateField()


























