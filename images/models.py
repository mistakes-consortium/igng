from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django_extensions.db.fields import ShortUUIDField
from imagekit.models.fields import ProcessedImageField
from imagekit.models.fields import ImageSpecField
from pilkit.processors.base import Transpose
from pilkit.processors.resize import ResizeToFill, SmartResize, Resize
from taggit.managers import TaggableManager

# User = get_user_model()
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Gallery(models.Model):
    user = models.ForeignKey(User)
    updated = models.DateTimeField(auto_now=True)

    # info fields
    rel_start = models.DateField(null=True, blank=True)
    rel_end = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)

    # status fields
    private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Image(models.Model):
    user = models.ForeignKey(User)
    gallery = models.ForeignKey(Gallery)
    uploaded = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=256, null=True, blank=True)

    tags = TaggableManager()
    uuid = ShortUUIDField(max_length=12)

    file = ProcessedImageField(
        upload_to="uploads",
        processors=[Transpose()],
        format="JPEG",
    )
    bigger = ImageSpecField(
        source="file",
        processors=[Resize(1440, 1080)],
        format="JPEG",
        options={'quality': 80}
    )
    default = ImageSpecField(
        source="file",
        processors=[Resize(720, 540)],
        format="JPEG",
        options={'quality': 80}
    )
    preview = ImageSpecField(
        source="file",
        processors=[SmartResize(320, 240)],
        format="JPEG",
        options={'quality': 80}
    )
    thumb = ImageSpecField(
        source="file",
        processors=[SmartResize(160, 120)],
        format="JPEG",
        options={'quality': 60},
    )
    tiny_thumb = ImageSpecField(
        source="file",
        processors=[SmartResize(80, 60)],
        format="JPEG",
        options={'quality': 40},
    )



class FeaturedImage(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)