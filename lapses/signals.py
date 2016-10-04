from images.models import Image

from django.db.models.signals import post_save
from django.dispatch import receiver

from lapses.tasks import autolapse


@receiver(post_save, sender=Image)
def do_the_lapse_hook(sender, instance, created, **kwargs):
    if created and instance.gallery.autolapse_configs.exists():
        autolapse.delay(instance.gallery.id)