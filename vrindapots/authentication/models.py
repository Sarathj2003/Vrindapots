from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    address = models.TextField(null=True)

    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

