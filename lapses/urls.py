from django.conf.urls import include, patterns, url
from rest_framework import routers
from lapses import views

urlpatterns = patterns(
    'lapses.views',
    url(r'^l/mk/(?P<gal_uuid>[\w-]+)$', views.mk_lapse, name="lapse_create"),
    url(r'^l/(?P<obj_uuid>[\w-]+)$', views.get_lapse, name="lapse_get"),
    url(r'^l/(?P<obj_uuid>[\w-]+)/settings', views.update_lapse, name="lapse_edit"),
)
