from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)  # Add an id field
    email=models.EmailField(max_length=50,unique=True,null=False)
    username=models.CharField(max_length=50)
    bio=models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    def __str__(self) :
        return self.username
   


