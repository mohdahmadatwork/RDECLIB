
from django.db import models
from django.contrib.auth.models import User

import uuid


# Create your models here.
class AddBook(models.Model):
    Date = models.DateField(auto_now_add=True)
    Accession_Number = models.AutoField(primary_key=True)
    Author = models.CharField(max_length=400)
    Title = models.CharField(max_length=500)
    Volume = models.IntegerField(blank=True,null=True)
    Place = models.CharField(max_length=500)
    Publisher = models.CharField(max_length=400)
    Year_Of_Publication = models.IntegerField(blank=True,null=True)
    Source = models.CharField(max_length=400,blank=True,null=True)
    Pages = models.IntegerField(blank=True,null=True)
    Book_Number = models.IntegerField()
    Bill_Number = models.IntegerField(blank=True,null=True)
    Bill_Date = models.DateField(blank=True,null=True)
    Withdrawn_Date = models.DateField(blank=True,null=True)
    Remark = models.CharField(max_length=1000,blank=True,null=True)
    class_No = models.IntegerField(blank=True,null=True)
    Category=models.CharField(max_length=100,default=" ")
    Available=models.BooleanField(default=True)
    def __str__(self) :
        return self.Title[0:50]

class AddStudent(models.Model):
    objectid=models.AutoField(primary_key=True,editable=False)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Fathers_Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=500)
    Roll_Number = models.BigIntegerField()
    Year = models.IntegerField(default=0)
    Branch=models.CharField(max_length=50)
    Phone_Number=models.BigIntegerField()
    Joining_Date=models.DateField()
    Expiring_Date=models.DateField()
    Library_ID = models.CharField(max_length=20,default=0)
    Student_image=models.ImageField(upload_to="img/",default="")
    Student_barcode=models.ImageField(upload_to="img/",default="")
    Email=models.CharField(max_length=200,default="Not Present")
    customuser=models.ForeignKey(to = User , on_delete=models.CASCADE)
    def __str__(self) :
        return self.First_Name
class Book_issued(models.Model):
    bookno=models.ForeignKey(to=AddBook,on_delete=models.CASCADE)
    Student=models.ForeignKey(to=AddStudent,on_delete=models.CASCADE)
    Date_Issue=models.DateTimeField(auto_now_add=True)
    Date_Return=models.DateTimeField(blank=True,null=True)
    Return_Status=models.BooleanField(default=False)

class Book_Return(models.Model):
    bookno=models.ForeignKey(to=AddBook,on_delete=models.CASCADE)
    Student=models.ForeignKey(to=AddStudent,on_delete=models.CASCADE)
    Date_Return=models.DateTimeField(auto_now_add=True)
    
class faculty(models.Model):
    Name = models.CharField(max_length=100)
    Faculty_image=models.ImageField(upload_to="img/",default="")
    Branch = models.CharField(max_length=100)
    Designation = models.CharField(max_length=50)
    Email = models.EmailField(unique=True,max_length=200 )
    Username = models.CharField(max_length=100,primary_key=True)
    Password = models.CharField(max_length=20)
    Confirm = models.BooleanField(default=False)
    customuser = models.ForeignKey(to= User , on_delete=models.CASCADE)
    
    

