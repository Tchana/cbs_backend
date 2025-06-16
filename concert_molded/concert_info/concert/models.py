from django.db import models

class Information(models.Model):
    nom = models.CharField(max_length=250)
    telephone = models.IntegerField()
    recevoirInfo = models.BooleanField(default=False)

    
    
   
    