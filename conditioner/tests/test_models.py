"""
Test 'conditioner.models' file
"""
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.test import TestCase

from conditioner.models import Rule
from conditioner.tests.factories import RuleFactory, BaseActionFactory, BaseConditionFactory
from conditioner.utils import TimeStampedModelMixin


class RuleTestCase(TestCase):
    """
    Test `conditioner.Rule` model
    """
    def setUp(self):
        super().setUp()
        self.model = Rule
        self.instance = RuleFactory()

        # Link sample action and condition to rule
        BaseActionFactory(rule=self.instance)
        BaseConditionFactory(rule=self.instance)

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, models.Model)
        self.assertIsInstance(self.instance, TimeStampedModelMixin)

    def test_model_target_content_type_field(self):
        """Test model 'target_content_type' field"""
        field = self.model._meta.get_field('target_content_type')

        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.rel.model, ContentType)
        self.assertEqual(field.rel.related_name, 'rules')
        self.assertEqual(field.verbose_name, 'target content type')
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_model_meta_attributes(self):
        """Test model meta attributes"""
        meta = self.model._meta

        self.assertEqual(meta.verbose_name, 'rule')
        self.assertEqual(meta.verbose_name_plural, 'rules')

    def test_model_target_model_property(self):
        """Test model `target_model()` property"""
        self.assertEqual(
            self.instance.target_model,
            self.instance.target_content_type.model_class()
        )

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertIn(str(self.instance.action), str(self.instance))
        self.assertIn(str(self.instance.condition), str(self.instance))
        self.assertIn(str(self.instance.target_model), str(self.instance))
