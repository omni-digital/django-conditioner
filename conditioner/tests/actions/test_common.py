"""
Test 'conditioner.actions.common' file
"""
from unittest import mock

from django.conf import settings
from django.db import models
from django.test import TestCase
from django.utils.crypto import get_random_string

from conditioner.actions.common import SendTemplatedEmailAction
from conditioner.base import BaseAction
from conditioner.tests.actions.factories import SendTemplatedEmailActionFactory


class LoggerActionTestCase(TestCase):
    """
    Test `conditioner.actions.common.SendTemplatedEmailAction` model
    """
    def setUp(self):
        super().setUp()
        self.model = SendTemplatedEmailAction
        self.instance = SendTemplatedEmailActionFactory()

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, BaseAction)

    def test_model_email_field(self):
        """Test model 'email' field"""
        field = self.model._meta.get_field('email')

        self.assertIsInstance(field, models.EmailField)
        self.assertEqual(field.verbose_name, 'email address')

    def test_model_subject_field(self):
        """Test model 'subject' field"""
        field = self.model._meta.get_field('subject')

        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.verbose_name, 'subject')
        self.assertEqual(field.max_length, 256)

    def test_model_template_field(self):
        """Test model 'template' field"""
        field = self.model._meta.get_field('template')

        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.verbose_name, 'template')
        self.assertEqual(field.max_length, 256)

    def test_model_meta_attributes(self):
        """Test model meta attributes"""
        meta = self.model._meta

        self.assertEqual(meta.verbose_name, 'send templated email action')
        self.assertEqual(meta.verbose_name_plural, 'send templated email actions')

    @mock.patch('conditioner.actions.common.get_available_templates')
    def test_model_available_templates_method(self, mocked_get_available_templates):
        """Test model `get_available_templates()` method"""
        self.instance.available_templates()

        mocked_get_available_templates.assert_called_once_with(
            'templates/conditioner/actions/emails/'
        )

    @mock.patch('conditioner.actions.common.EmailMultiAlternatives')
    @mock.patch('conditioner.actions.common.render_to_string')
    def test_model_run_action_method(self, mocked_render_to_string, mocked_email):
        """Test model `run_action()` method"""
        rendered_template = get_random_string()
        mocked_render_to_string.return_value = rendered_template

        self.instance.run_action()

        mocked_email.assert_called_once_with(
            subject=self.instance.subject,
            body=rendered_template,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.instance.email],
        )

        self.assertEqual(mocked_render_to_string.call_count, 2)
        mocked_render_to_string.assert_any_call(self.instance.template)
        mocked_render_to_string.assert_any_call(self.instance.template.replace('.txt', '.html'))

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertIn(self.instance.email, str(self.instance))
        self.assertIn(self.instance.template, str(self.instance))
