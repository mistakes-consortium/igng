from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'i_gng.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # move these to common if we have more than 3
    url(r'^a/settings$', 'common.views.user_settings', name="usersettings"),
    url(r'^a/settings/ui', 'common.views.user_settings_ui', name="usersettings_ui"),
    (r'^a/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i/', include("images.urls")),
    url(r'^t/', include("token_mgmt.urls")),

    url(r'^$', "images.views.index")
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
