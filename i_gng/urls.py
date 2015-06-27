from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'i_gng.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^a/settings', 'images.views.user_settings', name="usersettings"),
    (r'^a/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i/', include("images.urls")),

    url(r'$', "images.views.index")
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
