from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Row, HTML
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

class ImageSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('title'),
            'tags',
        )
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Image
        fields = ('title', 'tags')

class ImageSettingsTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageSettingsTagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<small class="hit comma if it doesn\'t autosuggest"></small>'),
            'tags',

        )
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Image
        fields = ('tags',)

class UserSettingsImageGalleryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(UserSettingsImageGalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'tags',

        )
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['gallery'].queryset = Gallery.objects.filter(user=user)

    class Meta:
        model = Image
        fields = ('gallery',)

# TODO validate the unique_together here :<
class GallerySettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GallerySettingsForm, self).__init__(*args, **kwargs)
        self.fields['display_density'].label = False
        self.fields['display_sort'].label = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Field("rel_start", css_class="datepicker"),
            Field("rel_end", css_class="datepicker"),
            Row(
                Field('display_density', label=None),
                Field('display_sort', label=None),
                Field('private'),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Gallery
        fields = ('rel_start', 'rel_end', 'title', 'display_density', 'display_sort', 'private')


class GalleryCreateForm(GallerySettingsForm):
    class Meta:
        model = Gallery
        fields = ('title', 'rel_start', 'rel_end', 'display_density', 'display_sort','private')

