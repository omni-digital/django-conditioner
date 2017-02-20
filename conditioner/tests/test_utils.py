"""
Test 'conditioner.utils' file
"""
from unittest import mock

from django.db import models
from django.test import TestCase

from conditioner.utils import TimeStampedModelMixin, get_available_templates


class TimeStampedModelMixinTestCase(TestCase):
    """
    Test `conditioner.utils.TimeStampedModelMixin` model
    """
    def setUp(self):
        super().setUp()
        self.model = TimeStampedModelMixin

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.model(), models.Model)

    def test_model_created_field(self):
        """Test model 'created' field"""
        field = self.model._meta.get_field('created')

        self.assertIsInstance(field, models.DateTimeField)
        self.assertEqual(field.verbose_name, 'created')
        self.assertFalse(field.editable)
        self.assertTrue(field.auto_now_add)

    def test_model_modified_field(self):
        """Test model 'modified' field"""
        field = self.model._meta.get_field('modified')

        self.assertIsInstance(field, models.DateTimeField)
        self.assertEqual(field.verbose_name, 'modified')
        self.assertFalse(field.editable)
        self.assertTrue(field.auto_now)

    def test_model_meta_attributes(self):
        """Test model meta attributes"""
        meta = self.model._meta

        self.assertTrue(meta.abstract)
        self.assertEqual(meta.get_latest_by, 'modified')
        self.assertEqual(meta.ordering, ('-modified', '-created'))


class GetAvailableTemplatesTestCase(TestCase):
    """
    Test 'conditioner.utils.get_available_templates` function
    """

    @mock.patch('os.path.isfile')
    @mock.patch('glob.glob')
    @mock.patch('conditioner.utils.get_app_template_dirs')
    def test_get_available_templates_function(self, mocked_get_app_template_dirs, mocked_glob, mocked_is_file):
        """Test `conditioner.utils.get_available_templates` function"""
        mocked_get_app_template_dirs.return_value = ['/template/dir']
        mocked_glob.return_value = ['/path/templates/subdir/test.txt', '/path/templates/example.txt']
        mocked_is_file.side_effect = [True, False]

        templates = get_available_templates('templates/example/path/')
        expected_templates = [
            ('subdir/test.txt', 'test (txt + html)'),
            ('example.txt', 'example (txt)'),
        ]

        self.assertEqual(templates, expected_templates)
        self.assertEqual(mocked_is_file.call_count, 2)
        self.assertEqual(mocked_glob.call_count, 1)
