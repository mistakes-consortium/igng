from django.contrib import admin

# Register your models here.
from lapses.models import AutoLapseConfiguration, AutoLapseInstance, AutoLapseInstanceFile

admin.site.register(AutoLapseConfiguration)
admin.site.register(AutoLapseInstance)
admin.site.register(AutoLapseInstanceFile)