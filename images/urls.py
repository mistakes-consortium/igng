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
    url(r'^g/mk/$', views.user_create_gallery, name="user_gallery_create"),
    url(r'^g/(?P<obj_uuid>[\w-]+)$', views.user_get_gallery_images, name="user_gallery_images"),
    url(r'^g/(?P<obj_uuid>[\w-]+)/toggle_priv$', views.user_gallery_priv_toggle, name="user_gallery_privacy_toggle"),
    url(r'^g/(?P<obj_uuid>[\w-]+)/settings', views.user_gallery_settings, name="user_gallery_settings"),
    url(r'^api/', include(router.urls, namespace='api')),
)