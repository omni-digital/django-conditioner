"""
Test 'conditioner.utils' file
"""
from unittest import mock

from django.test import TestCase

from conditioner.utils import get_available_templates


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
