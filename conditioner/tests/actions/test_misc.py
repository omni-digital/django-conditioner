"""
Test 'conditioner.actions.misc' file
"""
from django.db import models
from django.test import TestCase

from conditioner.actions.misc import LoggerAction
from conditioner.base import BaseAction
from conditioner.tests.actions.factories import LoggerActionFactory


class LoggerActionTestCase(TestCase):
    """
    Test `conditioner.actions.misc.LoggerAction` model
    """
    def setUp(self):
        super().setUp()
        self.model = LoggerAction
        self.instance = LoggerActionFactory()

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, BaseAction)

    def test_model_level_field(self):
        """Test model 'level' field"""
        field = self.model._meta.get_field('level')

        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.verbose_name, 'logging level')
        self.assertEqual(field.choices, self.model.LEVEL_CHOICES)
        self.assertEqual(field.max_length, 64)

    def test_model_message_field(self):
        """Test model 'message' field"""
        field = self.model._meta.get_field('message')

        self.assertIsInstance(field, models.TextField)
        self.assertEqual(field.verbose_name, 'message')

    def test_model_meta_attributes(self):
        """Test model meta attributes"""
        meta = self.model._meta

        self.assertEqual(meta.verbose_name, 'logger action')
        self.assertEqual(meta.verbose_name_plural, 'logger actions')

    def test_model_run_action_method(self):
        """Test model `run_action()` method"""
        logger_name = 'conditioner.actions.misc'
        with self.assertLogs(logger_name, level='DEBUG') as log:
            self.instance.run_action()

        self.assertEqual(len(log.records), 1)

        log_item = log.records[0]
        self.assertEqual(self.instance.level, log_item.levelname)
        self.assertEqual(self.instance.message, log_item.message)

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertIn(self.instance.level, str(self.instance))
        self.assertIn(self.instance.message[:20], str(self.instance))
