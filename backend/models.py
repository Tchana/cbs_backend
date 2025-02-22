from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import CustomUserManager

from django.contrib.auth import get_user_model


#

class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
        description of fields name of custom FIELDS of the table CustomUSer
        
        firstname : First Name of the user
        lastname : Last name of the user
        email : email of the user
        p_image : profil image of the user
        role : role of the user('admin', 'teacher', 'student')
        
    '''
    CHOICES = (('teacher', 'TEACHER'),
               ('student', 'STUDENT'),
               ('admin', 'ADMIN'),
               )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    p_image = models.ImageField(upload_to='profile_pictures')
    role = models.CharField(max_length=20, choices=CHOICES)

    ###Default fields####
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    ###Required fields###
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid3(uuid.NAMESPACE_DNS, self.email)
        super().save(*args, **kwargs)


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Course(models.Model):
    CHOICES = (('Level 1', 'level 1'),
               ('Level 2', 'Level 2'),
               ('Level 3', 'Level 3'))
    level = models.CharField(max_length=20, choices=CHOICES)
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.lower()
        super().save(*args, **kwargs)


class Enrollement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='registrations')
    registered_on = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='')
    description = models.TextField(max_length=500)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title


class Book(models.Model):
    CHOICES = (("bible", "bible"),
               ("commentary", "commentary"),
               ("random", "random")
               )
    title = models.CharField(max_length=100)
    book = models.FileField(upload_to='books')
    category = models.CharField(max_length=50, choices=CHOICES)
    book_cover = models.FileField(upload_to='book_cover')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title


class Audio(models.Model):
    title = models.CharField(max_length=100)
    audio = models.FileField(upload_to='teaching', unique=True)

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.lower()
        super().save(*args, **kwargs)


class Video(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='teaching', unique=True)

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.lower()
        super().save(*args, **kwargs)
