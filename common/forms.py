from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Row
from django import forms
from enumfields.fields import EnumField

from common.models import UserProfile, UISettinsEnum


class ProfileUIForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUIForm, self).__init__(*args, **kwargs)
        self.fields['ui_darkness'].label = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("ui_darkness", label="DARK")
        )
        self.helper.add_input(Submit('submit', 'Save'))

    ui_darkness = EnumField(UISettinsEnum, max_length=1).formfield(empty_label=None)

    class Meta:
        model = UserProfile
        fields = ('ui_darkness',)
