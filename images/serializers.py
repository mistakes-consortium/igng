import datetime
from images.models import Gallery, Image
from rest_framework import serializers
import pytz


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('uuid', 'user', 'updated', 'updated_u', 'rel_start', 'rel_end', 'title', 'private')

    updated_u = serializers.SerializerMethodField()

    def get_updated_u(self, obj):
        return (obj.updated - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()


class ImageSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()
    thumb_url = serializers.SerializerMethodField()
    tiny_thumb_url = serializers.SerializerMethodField()
    gallery = serializers.CharField(source="gallery.uuid")

    uploaded_u = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('uuid', 'user', 'gallery', 'uploaded', 'uploaded_u', 'title', 'uuid',
                  'full_url', 'thumb_url', 'tiny_thumb_url')

    def get_full_url(self, obj):
        return obj.full_fixed.url

    def get_thumb_url(self, obj):
        return obj.thumb.url

    def get_tiny_thumb_url(self, obj):
        return obj.tiny_thumb.url

    def get_uploaded_u(self, obj):
        return (obj.uploaded - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()