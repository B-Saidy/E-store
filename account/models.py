from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(blank=True,null=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    image = models.ImageField(upload_to = 'photos', default ='about.jpg')
    
    def __str__(self):
        return f"{self.user.username} profile"