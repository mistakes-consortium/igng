from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Row
from crispy_forms_materialize.layout import FileField
from django import forms

from lapses.models import AutoLapseConfiguration


class LapseCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LapseCreateForm, self).__init__(*args, **kwargs)
        self.fields['max_output_size'].label = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'create_new_every',
            'image_count',
            'frames_per_second',
            Row(
                Field('enabled', label=None),
                Field('max_output_size', label=None),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = AutoLapseConfiguration
        fields = ('create_new_every', 'image_count', 'frames_per_second', 'enabled', 'max_output_size')