from rest_framework import routers
from images import api

router = routers.DefaultRouter()
router.register(r'public/gallery', api.PublicGalleryViewSet, base_name="galleries_public")
router.register(r'user/gallery', api.UserGalleryViewSet, base_name="galleries_all")
router.register(r'user/images', api.ImageViewSet, base_name="images_all")
urlpatterns = router.urls
# urlpatterns += patterns('weblog.views',
#     url(r'^tag/(?P<tag>\w+)/$', 'tag'),
# )