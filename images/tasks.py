from celery import shared_task
from images.models import Image


@shared_task
def generate_thumbs(image_id,f=True, b=True, d=True, p=True,t=True,tt=True):
    i = Image.objects.get(pk=image_id)
    if f:
        i.full_fixed.generate()
    if b:
        i.bigger.generate()
    if d:
        i.default.generate()
    if p:
        i.preview.generate()
    if t:
        i.thumb.generate()
    if tt:
        i.tiny_thumb.generate()

@shared_task
def retrieve_exif(image_id):
    i = Image.objects.get(pk=image_id)
    i.query_exif()
