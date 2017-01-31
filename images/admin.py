from bitfield.forms import BitFieldCheckboxSelectMultiple
from bitfield import BitField
from django.contrib import admin

# Register your models here.
from imagekit.admin import AdminThumbnail
from images.models import Image, Gallery, FeaturedImage


def run_exif(modeladmin, request, queryset):
    for o in queryset:
        o.query_exif(do_empty=True)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='tiny_thumb')
    actions = [run_exif]

    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery)
admin.site.register(FeaturedImage)