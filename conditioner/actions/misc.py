"""
Conditioner module actions misc models
"""
import logging

from django.db import models

from conditioner.base import BaseAction


logger = logging.getLogger(__name__)


class LoggerAction(BaseAction):
    """
    Class representation of a logger action

    It takes an logger level and message, and logs it when linked condition is met.
    """
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
    LEVEL_CHOICES = (
        (DEBUG, 'Debug'),
        (INFO, 'Info'),
        (WARNING, 'Warning'),
        (ERROR, 'Error'),
        (CRITICAL, 'Critical'),
    )
    level = models.CharField(
        verbose_name='logging level',
        choices=LEVEL_CHOICES,
        max_length=64,
    )

    message = models.TextField(
        verbose_name='message',
    )

    class Meta(BaseAction.Meta):
        verbose_name = 'logger action'
        verbose_name_plural = 'logger actions'

    def run_action(self, *args, **kwargs):
        """
        Log saved message with saved logging level
        """
        logging_func = getattr(logger, self.level.lower())
        logging_func(self.message)

    def __str__(self):
        return 'Logger action ({0.level}: {0.message:.20})'.format(self)
