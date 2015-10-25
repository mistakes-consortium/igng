from django.conf.urls import include, patterns, url
from token_mgmt import views

urlpatterns = patterns('images.views',
    url(r'^$', views.token_mgmt_basic_list, name="token_list"),
    url(r'^mk/$', views.token_mgmt_basic_create, name="token_add"),
    url(r'^rm/(?P<id>[\w-]+)$', views.token_mgmt_basic_remove, name="token_remove"),

)