"""
Test 'conditioner.actions.forms' file
"""
from django import forms
from django.test import TestCase

from conditioner.actions import SendTemplatedEmailAction
from conditioner.actions.forms import SendTemplatedEmailActionModelForm


class SendTemplatedEmailActionModelFormTestCase(TestCase):
    """
    Test `conditioner.actions.forms.SendTemplatedEmailActionModelForm` form
    """
    def setUp(self):
        super().setUp()
        self.form = SendTemplatedEmailActionModelForm
        self.instance = SendTemplatedEmailActionModelForm()

    def test_form_inheritance(self):
        """Test form inheritance"""
        self.assertIsInstance(self.instance, forms.ModelForm)

    def test_form_template_field_choices(self):
        """Test form 'template' field choices"""
        self.assertIsInstance(self.instance.fields['template'].widget, forms.Select)
        self.assertEqual(
            self.instance.fields['template'].widget.choices,
            SendTemplatedEmailAction.available_templates()
        )

    def test_form_meta_attributes(self):
        """Test form meta attributes"""
        meta = self.form._meta

        self.assertEqual(meta.model, SendTemplatedEmailAction)
        self.assertIsNone(meta.fields)  # '__all__' is translated to None in the background
