"""
Test 'conditioner.conditions.dates' file
"""
from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models
from django.test import TestCase

from freezegun import freeze_time

from conditioner.conditions.dates import DayOfMonthCondition, DayOfWeekCondition
from conditioner.base import BaseCronCondition
from conditioner.tests.conditions.factories import DayOfMonthConditionFactory, DayOfWeekConditionFactory


class DayOfMonthConditionTestCase(TestCase):
    """
    Test `conditioner.conditions.dates.DayOfMonthCondition` model
    """
    def setUp(self):
        super().setUp()
        self.model = DayOfMonthCondition
        self.instance = DayOfMonthConditionFactory()

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, BaseCronCondition)

    def test_model_day_field(self):
        """Test model 'day' field"""
        field = self.model._meta.get_field('day')

        self.assertIsInstance(field, models.PositiveSmallIntegerField)
        self.assertEqual(field.verbose_name, 'day of the month')
        self.assertEqual(field.help_text, "Action will occur every month on that day.")

    def test_model_day_field_validators(self):
        """Test model 'day' field validators"""
        field = self.instance._meta.get_field('day')
        validator = field.validators[0]

        self.assertIsInstance(validator, MaxValueValidator)
        self.assertEqual(validator.limit_value, 31)

    def test_model_meta_attributes(self):
        """Test model meta attributes"""
        meta = self.model._meta

        self.assertEqual(meta.verbose_name, 'day of month condition')
        self.assertEqual(meta.verbose_name_plural, 'day of month conditions')

    def test_model_is_met_method(self):
        """Test model `is_met()` method"""
        instance = DayOfMonthConditionFactory(day=2)

        # Wrong day
        with freeze_time('2016-01-01'):
            self.assertFalse(instance.is_met())

        # Correct day
        with freeze_time('2016-01-02'):
            self.assertTrue(instance.is_met())

        instance.last_executed = datetime(2016, 1, 2)
        instance.save()

        # Correct day, but the same date as 'last_executed'
        with freeze_time('2016-01-02'):
            self.assertFalse(instance.is_met())

        # Wrong day
        with freeze_time('2016-02-01'):
            self.assertFalse(instance.is_met())

        # Correct day
        with freeze_time('2016-02-02'):
            self.assertTrue(instance.is_met())

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertIn(str(self.instance.day), str(self.instance))


class DayOfWeekConditionTestCase(TestCase):
    """
    Test `conditioner.conditions.dates.DayOfWeekCondition` model
    """
    def setUp(self):
        super().setUp()
        self.model = DayOfWeekCondition
        self.instance = DayOfWeekConditionFactory()

    def test_model_inheritance(self):
        """Test model inheritance"""
        self.assertIsInstance(self.instance, BaseCronCondition)

    def test_model_weekday_field(self):
        """Test model 'weekday' field"""
        field = self.model._meta.get_field('weekday')

        self.assertIsInstance(field, models.PositiveSmallIntegerField)
        self.assertEqual(field.verbose_name, 'day of the week')
        self.assertEqual(field.choices, self.model.WEEKDAY_CHOICES)
        self.assertEqual(field.help_text, "Action will occur every week on that day.")

    def test_model_meta_attributes(self):
        """Test model meta attributes"""
        meta = self.model._meta

        self.assertEqual(meta.verbose_name, 'day of week condition')
        self.assertEqual(meta.verbose_name_plural, 'day of week conditions')

    def test_model_is_met_method(self):
        """Test model `is_met()` method"""
        instance = DayOfWeekConditionFactory(weekday=7)

        # Wrong weekday (January 1 2007 is Monday)
        with freeze_time('2007-01-01'):
            self.assertFalse(instance.is_met())

        # Correct weekday
        with freeze_time('2007-01-07'):
            self.assertTrue(instance.is_met())

        instance.last_executed = datetime(2007, 1, 7)
        instance.save()

        # Correct weekday, but the same date as 'last_executed'
        with freeze_time('2007-01-07'):
            self.assertFalse(instance.is_met())

        # Wrong weekday
        with freeze_time('2007-01-10'):
            self.assertFalse(instance.is_met())

        # Correct weekday
        with freeze_time('2007-01-14'):
            self.assertTrue(instance.is_met())

    def test_model_str_method(self):
        """Test model `__str__` method"""
        self.assertIn(self.instance.get_weekday_display(), str(self.instance))
