import base64
from datetime import datetime

from bitfield import BitField
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django_extensions.db.fields import ShortUUIDField
from enumfields import EnumIntegerField, Enum
from imagekit.cachefiles import ImageCacheFile
from imagekit.models.fields import ProcessedImageField
from imagekit.models.fields import ImageSpecField
from pilkit.processors.base import Transpose
from pilkit.processors.resize import ResizeToFill, SmartResize, Resize, ResizeToCover
from PIL import Image as IMG  # prevents clobbering of my namespace
from PIL.ExifTags import TAGS
import shortuuid
# from taggit.managers import TaggableManager
from taggit_autosuggest.managers import TaggableManager


# User = get_user_model()
from django.conf import settings
from images.managers import GalleryManager

User = settings.AUTH_USER_MODEL


class Gallery(models.Model):
    user = models.ForeignKey(User, related_name="galleries")
    updated = models.DateTimeField(auto_now=True)

    # other fields
    uuid = ShortUUIDField(db_index=True)

    # info fields
    rel_start = models.DateField(null=True, blank=True, verbose_name="Time Period Start")
    rel_end = models.DateField(null=True, blank=True, verbose_name="Time Period End")
    title = models.CharField(max_length=256, null=True, blank=True)

    # status fields
    private = models.BooleanField(default=True)

    # deletable
    deletable = models.BooleanField(default=True)

    # let the user pick how many cards to show in a gallery.
    @property
    def display_card_class(self):
        return [self.DisplaySize.TINY, self.DisplaySize.SMALL, self.DisplaySize.MEDIUM, self.DisplaySize.LARGE]
    @property
    def display_lapse_class(self):
        return [self.DisplaySize.LAPSE_SM, self.DisplaySize.LAPSE_LG]

    class DisplaySort(Enum):
        UPLOADED_ASC = 0
        UPLOADED_DSC = 1
        EXIF_ASC = 2
        EXIF_DSC = 3

        class Labels:
            UPLOADED_ASC = "Oldest Uploaded First"
            UPLOADED_DSC = "Newest Uploaded First"
            EXIF_ASC = "Taken First"
            EXIF_DSC = "Taken Last"

    class DisplaySize(Enum):
        TINY = 0
        SMALL = 1
        MEDIUM = 2
        LARGE = 3
        LAPSE_SM = 4
        LAPSE_LG = 5

        class Labels:
            TINY = "Twelve Images Per Row"
            SMALL = "Six Images Per Row"
            MEDIUM = "Three Images Per Row"
            LARGE = "Two Images Per Row"
            LAPSE_SM = "Ultra Compact Lapse Layout"
            LAPSE_LG = "Less Compact Lapse Layout"

    display_density = EnumIntegerField(DisplaySize, default=2)
    display_sort = EnumIntegerField(DisplaySort, default=0)

    def __unicode__(self):
        return self.title

    objects = GalleryManager()

    class Meta:
        unique_together = ('user', 'title')

    @property
    def has_images(self):
        return self.images.exists()

    @property
    def rand_img(self):
        return self.images.order_by("?")[0]

    @property
    def gallery_pagination_count(self):
        if self.display_density == Gallery.DisplaySize.TINY:
            return 36
        elif self.display_density == Gallery.DisplaySize.SMALL:
            return 24
        elif self.display_density == Gallery.DisplaySize.MEDIUM:
            return 12
        elif self.display_density == Gallery.DisplaySize.LARGE:
            return 16
        elif self.display_density == Gallery.DisplaySize.LAPSE_LG:
            return 25 * 8
        elif self.display_density == Gallery.DisplaySize.LAPSE_SM:
            return 29 * 15

    @property
    def template_display_class(self):
        if self.display_density == Gallery.DisplaySize.TINY:
            return "s1 m1"
        elif self.display_density == Gallery.DisplaySize.SMALL:
            return "s2 m2"
        elif self.display_density == Gallery.DisplaySize.MEDIUM:
            return "s4 m4"
        elif self.display_density == Gallery.DisplaySize.LARGE:
            return "s6 m6"

        elif self.display_density == Gallery.DisplaySize.LAPSE_LG:
            return "60px"
        elif self.display_density == Gallery.DisplaySize.LAPSE_SM:
            return "40px"

    @property
    def template_divisibility(self):
        if self.display_density == Gallery.DisplaySize.TINY:
            return 12
        elif self.display_density == Gallery.DisplaySize.SMALL:
            return 6
        elif self.display_density == Gallery.DisplaySize.MEDIUM:
            return 3
        elif self.display_density == Gallery.DisplaySize.LARGE:
            return 2

    @property
    def display_sort_string(self):
        if self.display_sort == Gallery.DisplaySort.UPLOADED_ASC:
            return ["uploaded"]
        elif self.display_sort == Gallery.DisplaySort.UPLOADED_DSC:
            return ["-uploaded"]

        elif self.display_sort == Gallery.DisplaySort.EXIF_ASC:
            return ["exif_timestamp"]
        elif self.display_sort == Gallery.DisplaySort.EXIF_DSC:
            return ["-exif_timestamp"]

    @property
    def latest_lapses_exist(self):
        configs = self.autolapse_configs.all()
        return any([c.autolapse_instances.exists() for c in configs])

    @property
    def latest_lapse_instances_for_preview(self):
        # print "xyz"
        configs = self.autolapse_configs.all()
        inst = {}
        for c in configs:
            if c.autolapse_instances.exists():
                inst[c.uuid] = c.autolapse_instances.filter().latest()
            else:
                inst[c.uuid] = ""
        return inst

#
DisplaySize = Gallery.DisplaySize
DisplaySort = Gallery.DisplaySort

def set_image_name_on_upload(instance, filename):
    file_ext = filename.rsplit('.', 1)[1]
    file_name = shortuuid.uuid()
    return settings.MEDIA_ROOT + "/uploads/" + ".".join([file_name, file_ext])


class Image(models.Model):
    user = models.ForeignKey(User)
    gallery = models.ForeignKey(Gallery, related_name="images")
    uploaded = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=256, null=True, blank=True)

    tags = TaggableManager(blank=True)
    uuid = ShortUUIDField(db_index=True)

    original = models.ImageField(
        upload_to=set_image_name_on_upload,
    )

    _view_mapping = {
        "view.3d.180": "view_3d_180",
        "view.3d": "view_3d_360",
        "view.3d.360": "view_3d_360",
        "view.3d.sphere": "view_3d_360",
        "view.sphere": "view_3d_360",
        "view.pano": "view_2d_pano",
        "view.pan": "view_2d_pano",
        "view.panorama": "view_2d_pano",
        "view.panoramic": "view_2d_pano",
    }
    view_flags = BitField(
        flags=(
            ('view_3d_180', '180 Degrees 3D'),
            ('view_3d_360', '360 Degrees 3D'),
            ('view_2d_pano', 'Panoramic'),
        ), null=True
    )
    # for multiple tags we use the first
    view_default = models.CharField(max_length=32, null=True, blank=True)

    def self_uuid(self):
        return self.uuid

    full_fixed = ImageSpecField(
        source="original",
        processors=[Transpose()],
        format="JPEG",
    )
    bigger = ImageSpecField(
        source="full_fixed",
        processors=[ResizeToCover(1440
, 1080, upscale=False)],
        format="JPEG",
        options={'quality': 80, 'prefix':"b"}
    )
    default = ImageSpecField(
        source="full_fixed",
        processors=[ResizeToCover(720, 540, upscale=False)],
        format="JPEG",
        options={'quality': 80, 'prefix':"d"}
    )
    preview = ImageSpecField(
        source="full_fixed",
        processors=[SmartResize(320, 240)],
        format="JPEG",
        options={'quality': 80, 'prefix':"p"}
    )
    thumb = ImageSpecField(
        source="full_fixed",
        processors=[SmartResize(160, 120)],
        format="JPEG",
        options={'quality': 60, 'prefix':"t"},
    )
    tiny_thumb = ImageSpecField(
        source="full_fixed",
        processors=[SmartResize(80, 60)],
        format="JPEG",
        options={'quality': 40,  'prefix':"tt"},
    )

    AVAIL_SIZES = ["full_fixed", "bigger", "default", "preview", "thumb", "tiny_thumb"]
    AVAIL_INTS = [0,1,2,3,4,5]

    exif_data = models.ManyToManyField("EXIFEntry", blank=True)
    exif_timestamp = models.DateTimeField(null=True, blank=True)

    @property
    def uuid_as_b64(self):
        return base64.b64encode(self.uuid)

    def query_exif(self, only_when_empty=True, do_empty=False):
        image = IMG.open(self.original)

        if do_empty:
            self.exif_data.clear()

        if only_when_empty:
            do = not self.exif_data.exists()
        else:
            do = True

        if do:
            try:
                exif_raw = image._getexif()
            except: # no usable exif
                return
            # I guess this deals with the compactness, so it needs to be decoded?
            if exif_raw:
                exif_decoded = {TAGS.get(k): v for k, v in exif_raw.iteritems()}

                out = []
                for key, value in exif_decoded.iteritems():
                    ek, ck = ExifKey.objects.get_or_create(key=key)
                    ev, cv = ExifValue.objects.get_or_create(value=value)

                    ee, ce = EXIFEntry.objects.get_or_create(key=ek, value=ev)
                    self.exif_data.add(ee)

                    if key == "DateTime":
                        value_stf = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                        self.exif_timestamp = value_stf
                        self.save()
            else:
                pass # no exif

    def cached_full_fixed(self):
        generator = ImageCacheFile(self.full_fixed)
        return generator.generate()
    
    def cached_bigger(self):
        generator = ImageCacheFile(self.bigger)
        return generator.generate()
    
    def cached_default(self):
        generator = ImageCacheFile(self.default)
        return generator.generate()
    
    def cached_preview(self):
        generator = ImageCacheFile(self.preview)
        return generator.generate()
    
    def cached_thumb(self):
        generator = ImageCacheFile(self.thumb)
        return generator.generate()
    
    def cached_tiny_thumb(self):
        generator = ImageCacheFile(self.tiny_thumb)
        return generator.generate()

    def get_next_by_gallery_ordering(self):
        gallery = self.gallery
        gallery_sort = gallery.display_sort_string
        if gallery_sort == ['uploaded']:
            try:
                return self.get_next_by_uploaded(gallery=gallery)
            except:
                return None
        if gallery_sort == ['-uploaded']:
            try:
                return self.get_previous_by_uploaded(gallery=gallery)
            except:
                return None
        # todo add EXIF based sorting

    def get_prev_by_gallery_ordering(self):
        gallery = self.gallery
        gallery_sort = gallery.display_sort_string
        if gallery_sort == ['uploaded']:
            try:
                return self.get_previous_by_uploaded(gallery=gallery)
            except:
                return None
        if gallery_sort == ['-uploaded']:
            try:
                return self.get_next_by_uploaded(gallery=gallery)
            except:
                return None
        # todo add EXIF based sorting

class FeaturedImage(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)


# I can't think of a better way to deal with arbitrary exif data...
class ExifKey(models.Model):
    key = models.CharField(max_length=64, null=True, blank=True)

    def __unicode__(self):
        return self.key or "None"


class ExifValue(models.Model):
    value = models.TextField()

    def __unicode__(self):
        return self.value or "None"


class EXIFEntry(models.Model):
    key = models.ForeignKey(ExifKey)
    value = models.ForeignKey(ExifValue)

    def __unicode__(self):
        return "<ExifEntry(%s:%s)>" % (self.key, self.value)





### from images.signals import update_exif
from images.signals import create_default_gallery