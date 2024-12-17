from django.db import models

# Create your models here.

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    link = models.CharField(max_length=300)
 
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=20)
   
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    tutor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    
class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title =  models.CharField(max_length=50)
    number = models.IntegerField()
    description  = models.TextField(blank=True)
    
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=20)

    
    

    
