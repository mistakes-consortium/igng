from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from images.models import Gallery, Image
from images.serializers import GallerySerializer, ImageSerializer, ImageUploadSerializer


class PublicGalleryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()
    lookup_field = "uuid"

    def filter_queryset(self, queryset):
        qs = super(PublicGalleryViewSet, self).filter_queryset(queryset)
        if self.request.user.is_authenticated():
            qs = qs.filter(Q(private=False) | Q(user=self.request.user))
        else:
            qs = qs.filter(Q(private=False))
        return qs


class UserGalleryViewSet(viewsets.ModelViewSet):
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def filter_queryset(self, queryset):
        qs = super(UserGalleryViewSet, self).filter_queryset(queryset)
        if self.request.user.is_authenticated():
            qs = qs.filter(Q(private=False) | Q(user=self.request.user))
        else:
            qs = qs.filter(Q(private=False))
        return qs

    # other routes
    @detail_route(methods=['GET'])
    def images(self, request, uuid=None):
        obj = self.get_object()
        return Response(ImageSerializer(data=obj.images, many=True).data)

    @detail_route(methods=['POST'])
    def toggle_private(self, request, uuid=None):
        obj = self.get_object()
        obj.private = not obj.private
        obj.save(update_fields=["private"])
        ret = {"status":"SUCCESS", "data":obj.private}
        return Response(ret)


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    lookup_field = "uuid"
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    # def filter_queryset(self, queryset):
    #     qs = super(ImageViewSet, self).filter_queryset(queryset)
    #     if self.request.user.is_authenticated():
    #         qs = qs.filter(Q(private=False) | Q(user=self.request.user))
    #     else:
    #         qs = qs.filter(Q(private=False))
    #     return qs

    def create(self, request, *args, **kwargs):
        self.serializer_class = ImageUploadSerializer
        super(ImageViewSet, self).create(request, *args, **kwargs)

    @detail_route(methods=['GET'])
    def exif_check(self, request, uuid=None):
        obj = self.get_object()
        obj.query_exif()

        ret = {"status":"EXIF_QUERIED"}
        return Response(ret, status=status.HTTP_201_CREATED)