from django.contrib import admin

# Register your models here.
from imagekit.admin import AdminThumbnail
from images.models import Image, Gallery, FeaturedImage

class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__','admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='tiny_thumb')


admin.site.register(Image,ImageAdmin)
admin.site.register(Gallery)
admin.site.register(FeaturedImage)