import datetime

from rest_framework.reverse import reverse

from images.fields import Base64ImageField
from images.models import Gallery, Image, EXIFEntry
from rest_framework import serializers
import pytz


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('uuid', 'user', 'updated', 'updated_u', 'rel_start', 'rel_end', 'title', 'private')

    updated_u = serializers.SerializerMethodField()

    def get_updated_u(self, obj):
        return (obj.updated - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()


class EXIFSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source="key.key")
    value = serializers.CharField(source="value.value")

    class Meta:
        model = EXIFEntry
        fields = ('key', 'value')


class ImageSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()
    thumb_url = serializers.SerializerMethodField()
    tiny_thumb_url = serializers.SerializerMethodField()
    gallery = serializers.CharField(source="gallery.uuid")

    uploaded_u = serializers.SerializerMethodField()
    exif_data = EXIFSerializer(read_only=True, many=True)

    class Meta:
        model = Image
        fields = ('uuid', 'user', 'gallery', 'uploaded', 'uploaded_u', 'title', 'uuid',
                  'full_url', 'thumb_url', 'tiny_thumb_url', 'exif_data')

    def get_full_url(self, obj):
        return obj.full_fixed.url

    def get_thumb_url(self, obj):
        return obj.thumb.url

    def get_tiny_thumb_url(self, obj):
        return obj.tiny_thumb.url

    def get_uploaded_u(self, obj):
        return (obj.uploaded - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()


class ImageUploadSerializer(serializers.ModelSerializer):
    original = serializers.FileField()

    class Meta:
        model = Image
        fields = ('user', 'gallery', 'title', 'original')

class PasteImageUploadSerializer(serializers.ModelSerializer):
    original = Base64ImageField(max_length=None, use_url=True,)
    class Meta:
        model = Image
        fields = ('original',)

class PasteReturnSerializer(serializers.ModelSerializer):
    tiny_thumb_url = serializers.SerializerMethodField()
    image_page = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ('tiny_thumb_url', 'image_page')
        # fields = ("original", )

    def get_tiny_thumb_url(self, obj):
        # print dir(obj)
        return obj.tiny_thumb.url

    def get_image_page(self, obj):
        return reverse("upload_success", args=[obj.uuid])