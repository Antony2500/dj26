from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Person, Stuff)
class Index(admin.ModelAdmin):
    pass