"""
Conditioner module conditions related factories
"""
import random

from conditioner.conditions import DayOfMonthCondition, DayOfWeekCondition, ModelSignalCondition
from conditioner.tests.factories import BaseConditionFactory, BaseCronConditionFactory


class DayOfMonthConditionFactory(BaseCronConditionFactory):
    """
    Factory for `conditioner.conditions.dates.DayOfMonthCondition` model
    """
    day = random.randint(1, 31)

    class Meta:
        model = DayOfMonthCondition


class DayOfWeekConditionFactory(BaseCronConditionFactory):
    """
    Factory for `conditioner.conditions.dates.DayOfWeekCondition` model
    """
    weekday = random.randint(1, 7)

    class Meta:
        model = DayOfWeekCondition


class ModelSignalConditionFactory(BaseConditionFactory):
    """
    Factory for `conditioner.conditions.signals.ModelSignalCondition` model
    """
    signal = random.choice([
        ModelSignalCondition.PRE_SAVE, ModelSignalCondition.POST_SAVE,
        ModelSignalCondition.PRE_DELETE, ModelSignalCondition.POST_DELETE,
        ModelSignalCondition.PRE_INIT, ModelSignalCondition.POST_INIT,
    ])

    class Meta:
        model = ModelSignalCondition
