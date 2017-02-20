"""
Conditioner module related utils
"""
import glob
import os

from django.db import models
from django.template.utils import get_app_template_dirs


class TimeStampedModelMixin(models.Model):
    """
    An abstract base class model that provides self managed 'created' and 'modified' fields.

    Based on:
        https://github.com/django-extensions/django-extensions/blob/master/django_extensions/db/models.py
    """
    created = models.DateTimeField(
        verbose_name='created',
        editable=False,
        auto_now_add=True,
    )

    modified = models.DateTimeField(
        verbose_name='modified',
        editable=False,
        auto_now=True,
    )

    class Meta:
        abstract = True
        get_latest_by = 'modified'
        ordering = ('-modified', '-created')


def get_available_templates(template_dir):
    """
    Helper method for returning a list of available email templates. Template needs to be a `*.txt` file and can have
    a HTML counterpart.

    :return: list of available email templates paths
    :rtype: list of tuples
    """
    templates_dir = get_app_template_dirs(template_dir)

    txt_templates = list()
    for template_dir in templates_dir:
        txt_templates += glob.glob(
            os.path.join(template_dir, '*.txt')
        )

    templates = list()
    for template in txt_templates:
        file_name, _ = os.path.splitext(os.path.basename(template))

        is_html_available = os.path.isfile(template.replace('.txt', '.html'))
        if is_html_available:
            label = '{} (txt + html)'.format(file_name)
        else:
            label = '{} (txt)'.format(file_name)

        templates.append(
            (template.split('templates/')[1], label)
        )

    return templates
