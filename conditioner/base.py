"""
Conditioner module base models
"""
from django.db import models

from polymorphic.models import PolymorphicModel


# Actions
class BaseAction(PolymorphicModel):
    """
    Class representation of a base action

    Should not be used directly and all actions must inherit from it.
    """
    rule = models.OneToOneField(
        'conditioner.Rule', related_name='action',
        verbose_name='rule',
    )

    @staticmethod
    def model_specific():
        """
        Returns model class (that inherits from `BaseAction`) if action is meant to be model specific and relies on
        model instances being passed to `run_action()`, `True` if it requires any model and `False` if the action is
        generic (default).
        """
        return False

    def run_action(self, *args, **kwargs):
        """
        Implements the actual action
        """
        raise NotImplementedError(
            "You have to implement 'run_action()' in all actions that inherit from 'BaseAction'"
        )

    def __str__(self):
        return 'Action'


# Conditions
class BaseCondition(PolymorphicModel):
    """
    Class representation of a base condition

    Should not be used directly and all conditions must inherit from it.
    """
    rule = models.OneToOneField(
        'conditioner.Rule', related_name='condition',
        verbose_name='rule',
    )

    @staticmethod
    def model_specific():
        """
        Returns model class (that inherits from `BaseCondition`) if action is meant to be model specific, `True` if it
        requires any model and `False` if the condition is generic (default).
        """
        return False

    def __str__(self):
        return 'Condition'


class BaseCronCondition(BaseCondition):
    """
    Class representation of a base cron condition

    Should not be used directly and all cron related conditions must inherit from it.
    """
    last_executed = models.DateTimeField(
        verbose_name='last executed',
        null=True,
        editable=False,
    )

    def is_met(self, *args, **kwargs):
        """
        Implements if the condition is met
        """
        raise NotImplementedError(
            "You have to implement 'is_met()' in all actions that inherit from 'BaseCronCondition'"
        )

    def __str__(self):
        return 'Cron condition'
