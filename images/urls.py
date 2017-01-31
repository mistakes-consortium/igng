from django.conf.urls import include, patterns, url
from rest_framework import routers
from images import api, views

router = routers.DefaultRouter()
router.register(r'public/gallery', api.PublicGalleryViewSet, base_name="galleries_public")
router.register(r'user/gallery', api.UserGalleryViewSet, base_name="galleries_all")
router.register(r'user/images', api.ImageViewSet, base_name="images_all")
router.register(r'upload', api.PasteImageViewSet, base_name="images_all_upload")
# urlpatterns = router.urls
urlpatterns = patterns('images.views',
                       url(r'^$', views.index),
                       url(r'^u/$', views.upload, name="upload_img"),
                       url(r'^u/s/(?P<obj_uuid>[\w-]+)', views.upload_success, name="upload_success"),
                       url(r'^u/i/(?P<obj_uuid>[\w-]+)', views.image_detail, name="image_detail"),

                        # data sources
                       url(r'tt$', views.gallery_tooltip_info_view, name="ajax_tooltip_root_view"),
                       url(r'tt/(?P<obj_uuid>[\w-]+)$', views.gallery_tooltip_info_view, name="ajax_tooltip_detail_view"),
                       url(r'ex$', views.gallery_exif_info_view, name="ajax_exif_root_view"),
                       url(r'ex/(?P<obj_uuid>[\w-]+)$', views.gallery_exif_info_view, name="ajax_exif_detail_view"),

                        # tag related views
                       url(r'^t/u/$', views.tags_user_all,name="tags_user_all"),
                       url(r'^t/u/(?P<tag>[\w.-]+)$', views.tags_user_detail, name="tags_user_detail"),
                       url(r'^g/(?P<obj_uuid>[\w-]+)/t/$', views.tags_gallery_all, name="tags_gallery_all"),
                       url(r'^g/(?P<obj_uuid>[\w-]+)/t/(?P<tag>[\w.-]+)$', views.tags_gallery_detail, name="tags_gallery_detail"),

                        # other user pages
                       url(r'^i/$', views.user_default_gallery_images, name="user_images"),
                       url(r'^i/(?P<obj_uuid>[\w-]+)/settings/$', views.user_image_settings, name="user_image_settings"),

                        # gallery views
                       url(r'^g/$', views.user_galleries, name="user_galleries"),
                       url(r'^g/mk/$', views.user_create_gallery, name="user_gallery_create"),
                       url(r'^g/(?P<obj_uuid>[\w-]+)$', views.user_get_gallery_images, name="user_gallery_images"),
                       url(r'^g/up/(?P<gallery_uuid>[\w-]+)$', views.upload, name="user_gallery_upload"),
                       url(r'^g/(?P<obj_uuid>[\w-]+)/toggle_priv$', views.user_gallery_priv_toggle, name="user_gallery_privacy_toggle"),
                       url(r'^g/(?P<obj_uuid>[\w-]+)/settings', views.user_gallery_settings, name="user_gallery_settings"),
                        # galleryperma
                       url(r'^g/p/(?P<obj_uuid>[\w-]+)/', views.linked_gallery_view, name="gallery_permalink"),

                        # api
                       url(r'^api/', include(router.urls, namespace='api')),
                       )