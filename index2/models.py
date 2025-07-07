import uuid
from enum import Enum

from django.db import models


class Color(Enum):
    WHITE = "white"
    RED = "red"
    BLUE = "blue"

class Shade(Enum):
    BLUE = "blue-sky-light"


class GoITeeens(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.IntegerField(default=0, null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(blank=True, null=False)
    fav_music = models.URLField()
    is_available = models.BooleanField()


# class Profile(models.Model):
#     language = models.CharField(max_length=50)
#     email = models.EmailField(max_length=70,blank=True,unique=True)
#
#     def __str__(self):
#         return str(self.email)
#
# class User(models.Model):
#     name = models.CharField(max_length=50)
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.name)