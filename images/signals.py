# from django.contrib.auth import get_user_model
# forgive me for I have sinned, wanted to get this working
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from images.models import Image, Gallery
import time


# this doesn't actually work because its dumb.
# @receiver(post_save, sender=Image)
def update_exif(sender, instance, created, **kwargs):
    if created:
        instance.query_exif()

@receiver(post_save, sender=User)
def create_default_gallery(sender, instance, created, **kwargs):
    if created:
        Gallery.objects.create(
            user = instance,
            title = "Default",
            deletable=False,
        )