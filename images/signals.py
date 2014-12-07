from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from images.models import Image
import time


# this doesn't actually work because its dumb.
@receiver(post_save, sender=Image)
def update_exif(sender, instance, created, **kwargs):
    if created:
        instance.query_exif()
