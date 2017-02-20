"""
Test 'conditioner.base' file
"""
from django.db import models
from django.test import TestCase

from polymorphic.models import PolymorphicModel

from conditioner.base import BaseAction, BaseCondition, BaseCronCondition
from conditioner.models import Rule
from conditioner.tests.factories import BaseActionFactory, BaseConditionFactory, BaseCronConditionFactory


class BaseActionTestCase(TestCase):
    """
    Test `conditioner.base.BaseAction` model
    """
    def setUp(self):
        super().setUp()
        self.model = BaseAction
        self.instance = BaseActionFactory()

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, models.Model)
        self.assertIsInstance(self.instance, PolymorphicModel)

    def test_model_rule_field(self):
        """Test model 'rule' field"""
        field = self.model._meta.get_field('rule')

        self.assertIsInstance(field, models.OneToOneField)
        self.assertEqual(field.rel.model, Rule)
        self.assertEqual(field.rel.related_name, 'action')
        self.assertEqual(field.verbose_name, 'rule')

    def test_model_run_action_method(self):
        """Test model `run_action()` method"""
        self.assertRaises(NotImplementedError, self.instance.run_action)

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertEqual(str(self.instance), 'Action')


class BaseConditionTestCase(TestCase):
    """
    Test `conditioner.base.BaseCondition` model
    """
    def setUp(self):
        super().setUp()
        self.model = BaseCondition
        self.instance = BaseConditionFactory()

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, models.Model)
        self.assertIsInstance(self.instance, PolymorphicModel)

    def test_model_rule_field(self):
        """Test model 'rule' field"""
        field = self.model._meta.get_field('rule')

        self.assertIsInstance(field, models.OneToOneField)
        self.assertEqual(field.rel.model, Rule)
        self.assertEqual(field.rel.related_name, 'condition')
        self.assertEqual(field.verbose_name, 'rule')

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertEqual(str(self.instance), 'Condition')


class BaseCronConditionTestCase(TestCase):
    """
    Test `conditioner.base.BaseCronCondition` model
    """
    def setUp(self):
        super().setUp()
        self.model = BaseCronCondition
        self.instance = BaseCronConditionFactory()

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, BaseCondition)

    def test_model_last_executed_field(self):
        """Test model 'last_executed' field"""
        field = self.model._meta.get_field('last_executed')

        self.assertIsInstance(field, models.DateTimeField)
        self.assertEqual(field.verbose_name, 'last executed')
        self.assertTrue(field.null)
        self.assertFalse(field.editable)

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertEqual(str(self.instance), 'Cron condition')
