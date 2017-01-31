from celery import shared_task
from images.models import Image, Gallery
import os

@shared_task
def generate_thumbs(image_id,f=True, b=True, d=True, p=True,t=True,tt=True, force=False,delete=False):
    i = Image.objects.get(pk=image_id)
    if f:
        i.full_fixed.generate(force=force)
    if b:
        if delete: os.remove(i.bigger.file.name)
        i.bigger.generate(force=force)
    if d:
        if delete: os.remove(i.default.file.name)
        i.default.generate(force=force)
    if p:
        if delete: os.remove(i.preview.file.name)
        i.preview.generate(force=force)
    if t:
        if delete: os.remove(i.thumb.file.name)
        i.thumb.generate(force=force)
    if tt:
        if delete: os.remove(i.tiny_thumb.file.name)
        i.tiny_thumb.generate(force=force)

@shared_task
def retrieve_exif(image_id):
    i = Image.objects.get(pk=image_id)
    i.query_exif()

## >>> for i in imgs:
## ...   generate_thumbs.delay(i.pk,f=False,p=False,t=False,tt=False,force=True)

# imgs = Image.objects.all()
# for i in imgs:
#   os.remove(i.default.file.name)
#   os.remove(i.bigger.file.name)

@shared_task
def update_flags_post_save(instance_id):
    """this had to be done here because the post_save behaviour for the tagging engine is funky"""
    instance = Image.objects.get(pk=instance_id)
    image_as_qs = Image.objects.filter(pk=instance.pk)

    # iterate through tags to find flags
    flags_to_set = []
    for tag in instance.tags.all():
        if tag.name in Image._view_mapping:
            flags_to_set.append(Image._view_mapping[tag.name])

    # remove dupes
    flags_to_set = list(set(flags_to_set))
    #
    statement = 0
    for f in flags_to_set:
        statement = statement | getattr(Image.view_flags, f)

    image_as_qs.update(view_flags=statement)