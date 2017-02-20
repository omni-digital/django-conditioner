"""
Conditioner module actions related factories
"""
import random

import factory
from faker import Factory as FakerFactory

from conditioner.actions import LoggerAction, SendTemplatedEmailAction
from conditioner.tests.factories import BaseActionFactory


faker = FakerFactory.create()


class LoggerActionFactory(BaseActionFactory):
    """
    Factory for `conditioner.actions.misc.LoggerAction` model
    """
    level = random.choice(LoggerAction.LEVEL_CHOICES)[0]
    message = factory.LazyAttribute(lambda n: faker.paragraph())

    class Meta:
        model = LoggerAction


class SendTemplatedEmailActionFactory(BaseActionFactory):
    """
    Factory for `conditioner.actions.common.SendTemplatedEmailAction` model
    """
    email = factory.LazyAttribute(lambda n: faker.email())
    subject = factory.LazyAttribute(lambda n: faker.sentence())
    template = factory.LazyAttribute(lambda n: faker.uri_path() + '.txt')

    class Meta:
        model = SendTemplatedEmailAction
