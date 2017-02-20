#!/usr/bin/env python3
import random
import string
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


SETTINGS = dict(
    SECRET_KEY=''.join([random.SystemRandom().choice(string.digits + string.ascii_letters + string.punctuation)
                        for i in range(50)]),
    DEBUG=True,
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'conditioner',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
)


def run_tests(*test_args):
    """
    Helper method for initializing dummy Django application and running 'django-conditioner' tests
    """
    if not test_args:
        test_args = ['conditioner']

    if not settings.configured:
        settings.configure(**SETTINGS)

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(test_args)

    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
