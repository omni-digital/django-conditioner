"""
Conditioner module actions related forms
"""
from django import forms

from conditioner.actions.common import SendTemplatedEmailAction


class SendTemplatedEmailActionModelForm(forms.ModelForm):
    """
    Model form for `conditioner.actions.common.SendTemplatedEmailAction`
    """
    def __init__(self, *args, **kwargs):
        """
        Extends Django's default initialization and adds choices to 'template' field
        """
        super().__init__(*args, **kwargs)
        self.fields['template'].widget = forms.Select(choices=SendTemplatedEmailAction.available_templates())

    class Meta:
        model = SendTemplatedEmailAction
        fields = '__all__'
