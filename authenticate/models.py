from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(null=True, unique=True)
    image = models.ImageField(default = 'images/profiles/profile.jpeg', upload_to='images/profiles')
    code = models.PositiveIntegerField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return f'{self.follower.username} following {self.user.username}'