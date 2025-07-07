from django.contrib import admin

from .models import *

# Register your models here.

# @admin.register(User, Profile)
# class Index(admin.ModelAdmin):
#     pass

@admin.register(GoITeeens)
class MyModelAdmin(admin.ModelAdmin):
    # Налаштуйте інтерфейс адміністратора для MyModel
    list_display = ('id', 'price', 'email')  # Відобразити ці поля у вигляді списку
    list_filter = ('price',)  # Додайте фільтри для поля created_at
    search_fields = ('name', 'fav_music')  # Увімкніть пошук за назвою та описом
    actions = ['my_custom_action']
    def my_custom_action(self, request, queryset):
        # Спеціальна логіка для виконання дії
        pass