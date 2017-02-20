"""
Conditioner module common actions models
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string

from conditioner.base import BaseAction
from conditioner.utils import get_available_templates


class SendTemplatedEmailAction(BaseAction):
    """
    Class representation of a send templated email action

    It takes an email subject and email template (selected from available templates) and sends it to passed
    email address when linked condition is met.
    """
    email = models.EmailField(
        verbose_name='email address',
    )

    subject = models.CharField(
        verbose_name='subject',
        max_length=256,
    )

    template = models.CharField(
        verbose_name='template',
        max_length=256,
    )

    class Meta(BaseAction.Meta):
        verbose_name = 'send templated email action'
        verbose_name_plural = 'send templated email actions'

    @staticmethod
    def available_templates():
        """
        Helper method for returning a list of available email templates. Template needs to be a `*.txt` file with
        a possible HTML counterpart.

        :return: list of available email templates paths
        :rtype: list of tuples
        """
        return get_available_templates('templates/conditioner/actions/emails/')

    def run_action(self, *args, **kwargs):
        """
        Send selected email template
        """
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=render_to_string(self.template),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.email],
        )

        # Attach HTML template with the same name if it exists
        try:
            email.attach_alternative(
                content=render_to_string(self.template.replace('.txt', '.html')),
                mimetype='text/html',
            )
        except TemplateDoesNotExist:
            pass

        return email.send()

    def __str__(self):
        return 'Send templated email action ({0.email}: {0.template})'.format(self)
