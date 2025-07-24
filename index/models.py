from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    birthday = models.DateField()
    password = models.CharField(257)
    phone = models.CharField(max_length=12)


class Stuff(models.Model):
    stuff_name = models.CharField(max_length=35)
    stuff_desc = models.CharField(max_length=257)
    photo = models.CharField(max_length=100)
    price = models.IntegerField(validators=[MinValueValidator(1)])

    def publish(self):
        self.save()

    # def __str__(self):
    #     return f"{self.stuff_name}, {self.stuff_desc}"


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    code = models.CharField(max_length=10, default="")


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(validators=[MinValueValidator(1)])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title