from datetime import datetime

from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Person, Stuff, Author, Profile)
class Index(admin.ModelAdmin):
    pass


@admin.register(Article)
class Article(admin.ModelAdmin):
    list_display = ("short_title", "slug", "created_at")

    def short_title(self, obj):
        return obj.title[0:10]

    actions = ['created_at_action']
    def created_at_action(self, request, queryset):
        queryset.update(created_at=datetime.utcnow())

    short_title.short_description = "Title"


@admin.register(Book)
class Book(admin.ModelAdmin):
    filter_horizontal = ("authors",)

    list_display = ("title", "code")
    list_filter = ("title", "authors__name")
    search_fields = ("code", "title")


