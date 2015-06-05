from django.conf.urls import include, patterns, url
from rest_framework import routers
from images import api, views

router = routers.DefaultRouter()
router.register(r'public/gallery', api.PublicGalleryViewSet, base_name="galleries_public")
router.register(r'user/gallery', api.UserGalleryViewSet, base_name="galleries_all")
router.register(r'user/images', api.ImageViewSet, base_name="images_all")
# urlpatterns = router.urls
urlpatterns = patterns('images.views',
    url(r'^$', views.index),
    url(r'^u/$', views.upload, name="upload_img"),
    url(r'^u/s/(?P<obj_uuid>[\w-]+)', views.upload_success, name="upload_success"),
    url(r'^i/$', views.user_default_gallery_images, name="user_images"),
    url(r'^g/$', views.user_galleries, name="user_galleries"),
    url(r'^g/(?P<obj_uuid>[\w-]+)$', views.user_get_gallery_images, name="user_gallery_images"),
    url(r'^api/', include(router.urls, namespace='api')),
)