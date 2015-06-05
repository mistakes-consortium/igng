from django import forms
from images.models import Image


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'original', 'tags')
