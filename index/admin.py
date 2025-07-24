from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Person, Stuff, Author, Profile, Article)
class Index(admin.ModelAdmin):
    pass

@admin.register(Book)
class Book(admin.ModelAdmin):
    filter_horizontal = ("authors",)