from django import forms
from images.models import Image, Gallery


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'original', 'tags')


class GallerySettingsForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('rel_start', 'rel_end', 'title', 'display_density') #'private'