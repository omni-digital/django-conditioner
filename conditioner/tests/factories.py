"""
Conditioner module related factories
"""
from django.contrib.contenttypes.models import ContentType

import factory
from faker import Factory as FakerFactory

from conditioner.base import BaseAction, BaseCondition, BaseCronCondition


faker = FakerFactory.create()


class RuleFactory(factory.DjangoModelFactory):
    """
    Factory for `conditioner.Rule` model
    """
    target_content_type = factory.Iterator(ContentType.objects.all())

    class Meta:
        model = 'conditioner.Rule'


class BaseActionFactory(factory.DjangoModelFactory):
    """
    Factory for `conditioner.base.BaseAction` model
    """
    rule = factory.SubFactory(RuleFactory)

    class Meta:
        model = BaseAction


class BaseConditionFactory(factory.DjangoModelFactory):
    """
    Factory for `conditioner.base.BaseCondition` model
    """
    rule = factory.SubFactory(RuleFactory)

    class Meta:
        model = BaseCondition


class BaseCronConditionFactory(BaseConditionFactory):
    """
    Factory for `conditioner.base.BaseCronCondition` model
    """

    class Meta:
        model = BaseCronCondition
