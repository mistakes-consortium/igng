from celery import shared_task
from images.models import Image
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
