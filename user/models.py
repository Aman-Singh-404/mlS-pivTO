from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length = 10)
    gender = models.CharField(max_length = 1, choices = [("M", "Male"), ("F", "Female")], default='M')
    
    def __str__(self):
        return self.user.username