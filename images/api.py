from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
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

    def check_ownership_for_actions(self, request, obj):
        if request.user != obj.user:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['GET'])
    def default(self, request):
        g = self.queryset.filter(user=request.user, deletable=False).get()
        return Response(GallerySerializer(g).data)

    # other routes
    @detail_route(methods=['GET'])
    def images(self, request, uuid=None):
        obj = self.get_object()
        return Response(ImageSerializer(obj.images, many=True).data)

    @detail_route(methods=['POST'])
    def toggle_private(self, request, uuid=None):
        obj = self.get_object()
        self.check_ownership_for_actions(request, obj)

        obj.private = not obj.private
        obj.save(update_fields=["private"])
        ret = {"status":"SUCCESS", "data":obj.private}
        return Response(ret)
    
    @detail_route(methods=['POST'])
    def upload(self, request, uuid=None):
        obj = self.get_object()
        self.check_ownership_for_actions(request, obj)

        # force these
        request.data['gallery'] = obj.pk
        request.data['user'] = request.user.id

        serialized = ImageUploadSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            o = serialized.save()
            return Response({"msg":"Upload Success", 'data':serialized.data}, status=status.HTTP_201_CREATED)
        
        


    # overrides
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_ownership_for_actions(request, obj)

        if not obj.deletable:
            return Response({"msg":"Not Deletable"}, status=status.HTTP_401_UNAUTHORIZED)

        return super(UserGalleryViewSet, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super(UserGalleryViewSet, self).create(request, *args, **kwargs)



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