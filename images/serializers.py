from rest_framework import serializers
from images.models import Gallery, Image


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('uuid', 'user', 'updated', 'rel_start', 'rel_end', 'title', 'private')


class ImageSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()
    thumb_url = serializers.SerializerMethodField()
    tiny_thumb_url = serializers.SerializerMethodField()
    gallery = serializers.CharField(source="gallery.uuid")

    class Meta:
        model = Image
        fields = ('uuid', 'user', 'gallery', 'uploaded', 'title', 'uuid',
                  'full_url', 'thumb_url', 'tiny_thumb_url')

    def get_full_url(self, obj):
        return obj.full_fixed.url

    def get_thumb_url(self, obj):
        return obj.thumb.url

    def get_tiny_thumb_url(self, obj):
        return obj.tiny_thumb.url