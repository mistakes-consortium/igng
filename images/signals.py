# from django.contrib.auth import get_user_model
# forgive me for I have sinned, wanted to get this working
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch.dispatcher import receiver
from taggit.models import TaggedItem

from images.models import Image, Gallery
import time


# this doesn't actually work because its dumb.
# @receiver(post_save, sender=Image)
from images.tasks import generate_thumbs, retrieve_exif, update_flags_post_save


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

@receiver(post_save, sender=TaggedItem)
def set_tag_booleans_before_save(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(Image)
    if instance.content_type == ct:
        update_flags_post_save.delay(instance.object_id)
    # # reset flags
    # instance.view_flags = 0
    # # iterate through tags to find flags
    # flags_to_set = []
    # print instance.tagged_items.all()
    # for tag in instance.tags.all():
    #     if tag.name in sender._view_mapping:
    #         flags_to_set.append(sender._view_mapping[tag.name])
    #
    # # remove dupes
    # flags_to_set = list(set(flags_to_set))
    # #
    # statement = 0
    # for f in flags_to_set:
    #     statement = statement | getattr(Image.view_flags, f)
    #
    # print statement
    # image_as_qs = Image.objects.filter(pk=instance.pk)
    # image_as_qs.update(view_flags=statement)
    #
    # return instance

@receiver(post_save, sender=Image)
def generate_thumbs_via_celery(sender, instance, created, **kwargs):
    if created:
        generate_thumbs.delay(instance.pk)

@receiver(post_save, sender=Image)
def attempt_to_retrieve_exif(sender, instance, created, **kwargs):
    if created:
        retrieve_exif.delay(instance.pk)