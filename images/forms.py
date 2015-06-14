from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Row
from crispy_forms_materialize.layout import FileField
from django import forms
from images.models import Image, Gallery


class ImageUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FileField('original'),
            Div('title'),
            'tags',
        )
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Image
        fields = ('title', 'original', 'tags')


class GallerySettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GallerySettingsForm, self).__init__(*args, **kwargs)
        self.fields['display_density'].label = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Field("rel_start", css_class="datepicker"),
            Field("rel_end", css_class="datepicker"),
            Row(
                Field('display_density', label=None),
                Field('private'),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Gallery
        fields = ('rel_start', 'rel_end', 'title', 'display_density', 'private')


class GalleryCreateForm(GallerySettingsForm):
    class Meta:
        model = Gallery
        fields = ('title', 'rel_start', 'rel_end', 'display_density', 'private')