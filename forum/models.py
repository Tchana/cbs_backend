from django.db import models
from django.contrib.auth import get_user_model
from backend.models import *
import uuid

# Create your models here.

User = get_user_model()

class ChatGroup(models.Model):
    groupe_name = models.CharField(max_length=200)
    def __str__(self):
        return self.groupe_name
    
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages',on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.firstName} : {self.body}"
    
    class Meta:
        ordering = ['-created']
    
    