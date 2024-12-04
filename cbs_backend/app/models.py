from django.db import models

# Create your models here.

class Books(models.Model):
    books_title = models.CharField(max_length=50)
    books_description = models.CharField(max_length=50)
    books_image_name = models.CharField(max_length=50)
    books_category = models.CharField(max_length=50)
    
 

class Course(models.Model):
    course_title = models.CharField(max_length=50)
    course_tutor = models.CharField(max_length=50)
    course_description = models.CharField(max_length=50)
    
    
class Lesson(models.CharField):
    #stranger key from Courses table
    cours = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_title =  models.CharField(max_length=50)
    lesson_number = models.IntegerField()
    lesson_description  = models.TextField(blank=True)
    
   
    

    
