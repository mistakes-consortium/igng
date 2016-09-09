from celery import shared_task
from images.models import Image


@shared_task
def generate_thumbs(image_id,f=True, b=True, d=True, p=True,t=True,tt=True, force=False):
    i = Image.objects.get(pk=image_id)
    if f:
        i.full_fixed.generate(force=force)
    if b:
        i.bigger.generate(force=force)
    if d:
        i.default.generate(force=force)
    if p:
        i.preview.generate(force=force)
    if t:
        i.thumb.generate(force=force)
    if tt:
        i.tiny_thumb.generate(force=force)

@shared_task
def retrieve_exif(image_id):
    i = Image.objects.get(pk=image_id)
    i.query_exif()
