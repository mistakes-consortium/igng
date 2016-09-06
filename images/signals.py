# from django.contrib.auth import get_user_model
# forgive me for I have sinned, wanted to get this working
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from images.models import Image, Gallery
import time


# this doesn't actually work because its dumb.
# @receiver(post_save, sender=Image)
from images.tasks import generate_thumbs, retrieve_exif


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

@receiver(post_save, sender=Image)
def generate_thumbs_via_celery(sender, instance, created, **kwargs):
    if created:
        generate_thumbs.delay(instance.pk)

@receiver(post_save, sender=Image)
def attempt_to_retrieve_exif(sender, instance, created, **kwargs):
    if created:
        retrieve_exif.delay(instance.pk)