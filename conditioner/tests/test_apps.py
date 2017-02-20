"""
Test 'conditioner.apps' file
"""
from django.apps import AppConfig
from django.apps import apps as license_tracker_apps
from django.test import TestCase


class ConditionerAppConfigTestCase(TestCase):
    """
    Test 'conditioner' module `AppConfig` integration
    """
    def test_conditioner_app_config(self):
        """Test 'licenses' module `AppConfig` instance"""
        conditioner_app_config = license_tracker_apps.get_app_config('conditioner')

        self.assertIsInstance(conditioner_app_config, AppConfig)
        self.assertEqual(conditioner_app_config.name, 'conditioner')
        self.assertEqual(conditioner_app_config.verbose_name, 'Conditioner')
