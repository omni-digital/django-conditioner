"""
Conditioner module conditions signals related models
"""
import uuid

from django.db import models

from conditioner.base import BaseCondition


class ModelSignalCondition(BaseCondition):
    """
    Class representation of a model signal condition

    It mirrors available Django model signals and creates a given signal for linked rule content type, with
    linked action as signal receiver.
    """
    PRE_INIT = 'pre_init'
    POST_INIT = 'post_init'
    PRE_SAVE = 'pre_save'
    POST_SAVE = 'post_save'
    PRE_DELETE = 'pre_delete'
    POST_DELETE = 'post_delete'
    SIGNAL_CHOICES = (
        ('Save', (
            (PRE_SAVE, 'Before creation'),
            (POST_SAVE, 'After creation'),
        )),
        ('Delete', (
            (PRE_DELETE, 'Before deletion'),
            (POST_DELETE, 'After deletion'),
        )),
        ('Init', (
            (PRE_INIT, 'Before initialization'),
            (POST_INIT, 'After initialization'),
        )),
    )
    signal = models.CharField(
        verbose_name='signal',
        choices=SIGNAL_CHOICES,
        max_length=64,
    )

    dispatch_uid = models.UUIDField(
        verbose_name='dispatch ID',
        editable=False,
        default=uuid.uuid4,
    )

    class Meta(BaseCondition.Meta):
        verbose_name = 'model signal condition'
        verbose_name_plural = 'model signal conditions'

    @staticmethod
    def model_specific():
        """
        This action is model specific
        """
        return True

    def connect_signal(self):
        """
        Connect selected signal to rule's target model
        """
        if hasattr(self.rule, 'action'):
            signal = getattr(models.signals, self.signal)

            signal.connect(
                receiver=self.rule.action.run_action,
                sender=self.rule.target_model,
                dispatch_uid=self.dispatch_uid,
                weak=False,
            )

    def disconnects_signal(self):
        """
        Disconnect selected signal from rule's target model
        """
        if hasattr(self.rule, 'action'):
            signal = getattr(models.signals, self.signal)

            signal.disconnect(
                receiver=self.rule.action.run_action,
                sender=self.rule.target_model,
                dispatch_uid=self.dispatch_uid,
            )

    def __str__(self):
        return 'Model signal condition ({0.signal} for {0.rule.target_content_type})'.format(self)

    def save(self, *args, **kwargs):
        """
        Extends default `save()` behaviour and connects signal
        """
        if not self.pk:
            self.connect_signal()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Extends default `delete()` behaviour and disconnects signal
        """
        super_delete = super().delete(*args, **kwargs)
        self.disconnects_signal()  # After deletion to make sure that everything went OK
        return super_delete
