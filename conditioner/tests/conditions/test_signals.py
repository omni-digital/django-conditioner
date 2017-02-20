"""
Test 'conditioner.conditions.signals' file
"""
import uuid
from unittest import mock

from django.db import models
from django.test import TestCase

from conditioner.conditions.signals import ModelSignalCondition
from conditioner.base import BaseCondition
from conditioner.tests.conditions.factories import ModelSignalConditionFactory
from conditioner.tests.factories import RuleFactory, BaseActionFactory


class ModelSignalConditionTestCase(TestCase):
    """
    Test `conditioner.conditions.signals.ModelSignalCondition` model
    """
    def setUp(self):
        super().setUp()
        self.model = ModelSignalCondition
        self.instance = ModelSignalConditionFactory()

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, BaseCondition)

    def test_model_signal_field(self):
        """Test model 'signal' field"""
        field = self.model._meta.get_field('signal')

        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.verbose_name, 'signal')
        self.assertEqual(field.choices, self.model.SIGNAL_CHOICES)
        self.assertEqual(field.max_length, 64)

    def test_model_dispatch_uid_field(self):
        """Test model 'dispatch_uid' field"""
        field = self.model._meta.get_field('dispatch_uid')

        self.assertIsInstance(field, models.UUIDField)
        self.assertEqual(field.verbose_name, 'dispatch ID')
        self.assertFalse(field.editable)
        self.assertEqual(field.default, uuid.uuid4)

    def test_model_meta_attributes(self):
        """Test model meta attributes"""
        meta = self.model._meta

        self.assertEqual(meta.verbose_name, 'model signal condition')
        self.assertEqual(meta.verbose_name_plural, 'model signal conditions')

    @mock.patch('django.db.models.signals')
    def test_model_connect_signal_method(self, patched_signals):
        """Test model `connect_signal()` method"""
        mocked_signal = getattr(patched_signals, self.instance.signal)
        mocked_signal_connect = mock.Mock()
        mocked_signal.connect = mocked_signal_connect

        self.instance.rule = RuleFactory()
        self.instance.rule.action = BaseActionFactory()
        self.instance.connect_signal()

        mocked_signal_connect.assert_called_once_with(
            receiver=self.instance.rule.action.run_action,
            sender=self.instance.rule.target_model,
            dispatch_uid=self.instance.dispatch_uid,
            weak=False,
        )

    @mock.patch('django.db.models.signals')
    def test_model_disconnects_signal_method(self, patched_signals):
        """Test model `disconnects_signal()` method"""
        mocked_signal = getattr(patched_signals, self.instance.signal)
        mocked_signal_disconnect = mock.Mock()
        mocked_signal.disconnect = mocked_signal_disconnect

        self.instance.rule = RuleFactory()
        self.instance.rule.action = BaseActionFactory()
        self.instance.disconnects_signal()

        mocked_signal_disconnect.assert_called_once_with(
            receiver=self.instance.rule.action.run_action,
            sender=self.instance.rule.target_model,
            dispatch_uid=self.instance.dispatch_uid,
        )

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertIn(self.instance.signal, str(self.instance))
        self.assertIn(str(self.instance.rule.target_content_type), str(self.instance))

    @mock.patch('conditioner.conditions.signals.ModelSignalCondition.connect_signal')
    def test_model_save_method(self, mocked_connect_signal):
        """Test model `save()` method"""
        ModelSignalConditionFactory()

        self.assertEqual(mocked_connect_signal.call_count, 1)

    @mock.patch('conditioner.conditions.signals.ModelSignalCondition.disconnects_signal')
    def test_model_delete_method(self, mocked_disconnects_signal):
        """Test model `delete()` method"""
        ModelSignalConditionFactory().delete()

        self.assertEqual(mocked_disconnects_signal.call_count, 1)
