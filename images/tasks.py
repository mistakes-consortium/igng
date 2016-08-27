from celery import shared_task
from images.models import Image


@shared_task
def generate_thumbs(image_id):
    i = Image.objects.get(pk=image_id)
    i.full_fixed.generate()
    i.bigger.generate()
    i.default.generate()
    i.preview.generate()
    i.thumb.generate()
    i.tiny_thumb.generate()
