import datetime

from rest_framework.reverse import reverse
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from images.fields import Base64ImageField
from images.models import Gallery, Image, EXIFEntry
from rest_framework import serializers
import pytz


class GallerySerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
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


class ImageSerializer(TaggitSerializer, serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()
    thumb_url = serializers.SerializerMethodField()
    tiny_thumb_url = serializers.SerializerMethodField()
    gallery = serializers.CharField(source="gallery.uuid")

    uploaded_u = serializers.SerializerMethodField()
    exif_data = EXIFSerializer(read_only=True, many=True)
    tags = TagListSerializerField(required=False)
    uuid = serializers.CharField(read_only=True)

    class Meta:
        model = Image
        fields = ('uuid', 'user', 'gallery', 'uploaded', 'uploaded_u', 'title', 'uuid',
                  'full_url', 'thumb_url', 'tiny_thumb_url', 'exif_data', 'tags')

    def get_full_url(self, obj):
        return obj.full_fixed.url

    def get_thumb_url(self, obj):
        return obj.thumb.url

    def get_tiny_thumb_url(self, obj):
        return obj.tiny_thumb.url

    def get_uploaded_u(self, obj):
        return (obj.uploaded - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()


class ImageUploadSerializer(TaggitSerializer,serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    original = serializers.FileField()
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Image
        fields = ('user', 'gallery', 'title', 'original', 'tags')

class PasteImageUploadSerializer(serializers.ModelSerializer):
    original = Base64ImageField(max_length=None, use_url=True,)
    gallery = serializers.SlugRelatedField(required=False, queryset=Gallery.objects.all(),slug_field="uuid")


    def get_fields(self, *args, **kwargs):
        fields = super(PasteImageUploadSerializer, self).get_fields(*args, **kwargs)
        fields['gallery'].queryset = Gallery.objects.filter(user=(self.context['request'].user))
        return fields

    class Meta:
        model = Image
        fields = ('original', 'gallery')

    def validate_gallery(self, value):
        u = self.context['request'].user
        if u.galleries.filter(uuid=value.uuid).exists():
            # print "YAY"
            return value
        elif value == None:
            # print "NULL"
            return value
        # print "BOO  "
        raise serializers.ValidationError("Non-existent Gallery")


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