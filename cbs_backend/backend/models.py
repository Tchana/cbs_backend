from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from django.contrib.auth import get_user_model


class CustomUser(AbstractBaseUser, PermissionsMixin):
    CHOICES = (('teacher', 'TEACHER'),
               ('student', 'STUDENT'),
               ('admin', 'ADMIN'),
               )
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=20, choices=CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Course(models.Model):
    User = get_user_model()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    

class Book(models.Model):
    title = models.CharField(max_length=100)
    

    
    
    
