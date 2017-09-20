from django.conf.urls import include,  url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

from common import views as views_common
from images import views as views_index

urlpatterns = [
    # Examples:
    # url(r'^$', 'i_gng.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # move these to common if we have more than 3
    url(r'^a/settings$', views_common.user_settings, name="usersettings"),
    url(r'^a/settings/ui', views_common.user_settings_ui, name="usersettings_ui"),
    url(r'^a/', include('allauth.urls')),
    url(r'^ra/', include('rest_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i/', include("images.urls")),
    url(r'^l/', include("lapses.urls")),
    url(r'^t/', include("token_mgmt.urls")),

    url(r'^$', views_index.index),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
