from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
# Create your models here.


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField()
    
    def __str__(self):
        return self.user.first_name



class Alert(models.Model):
    alert_type = models.TextField()
    location = models.TextField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.location
