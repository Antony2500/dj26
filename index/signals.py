import re
from uuid import uuid4

from Tools.demo.mcast import sender
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Article


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(pre_save, sender=Article)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        # примітивний “slugify”: lowercase + тире замість пробілів + видалити небажані символи

        #TODO r'[^\w\s-]'
        #TODO означає «будь-який символ,
        # не буква/цифра/підкреслення (\w),
        # не пробіл (\s)
        # і не дефіс (-)».

        #TODO " Привіт, світ!  Засідання — 2025 "
        #TODO "привіт світ  засідання  2025"
        #TODO "привіт світ-засідання-2025"

        filtered_title = re.sub(r'[^\w\s-]', '', instance.title).strip().capitalize()
        filtered_title = re.sub(r'[-\s]+', '-', filtered_title)
        instance.title = filtered_title
        instance.slug = uuid4()