"""
Conditioner module models
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType

from conditioner.utils import TimeStampedModelMixin


class Rule(TimeStampedModelMixin, models.Model):
    """
    Class representation of generic rule with target, condition and action
    """
    target_content_type = models.ForeignKey(
        ContentType, related_name='rules',
        verbose_name='target content type',
        null=True,
        blank=True,
    )

    # There are reverse 'BaseAction' and 'BaseCondition' foreign keys to allow Django Admin inline form
    # handling (with polymorphism), and thus aren't enforced but *should* be considered required

    class Meta(TimeStampedModelMixin.Meta):
        verbose_name = 'rule'
        verbose_name_plural = 'rules'

    @property
    def target_model(self):
        """Helper property for returning target model class"""
        return self.target_content_type.model_class() if self.target_content_type else None

    def __str__(self):
        if hasattr(self, 'action') and hasattr(self, 'condition'):
            return "Do '{0.action}' to '{0.target_model}' when '{0.condition}'".format(self)

        return 'Rule for {0.target_content_type}'.format(self)
