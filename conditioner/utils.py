"""
Conditioner module related utils
"""
import glob
import os

from django.template.utils import get_app_template_dirs


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
