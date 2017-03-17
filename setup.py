import io
import os
import re

from setuptools import setup, find_packages


# Convert description from markdown to reStructuredText
try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst', 'markdown')
except (OSError, ImportError):
    description = ''


# Get package version number
# Source: https://packaging.python.org/single_source_version/
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-conditioner',
    url='https://github.com/omni-digital/django-conditioner',
    download_url='https://github.com/omni-digital/django-conditioner/releases/latest',
    bugtrack_url='https://github.com/omni-digital/django-conditioner/issues',
    version=find_version('conditioner', '__init__.py'),
    license='MIT License',
    author='Omni Digital',
    author_email='dev@omni-digital.co.uk',
    maintainer='Omni Digital',
    maintainer_email='dev@omni-digital.co.uk',
    description="Create simple 'if this then that' style rules in your Django application. Comes with a bunch of "
                "ready to use actions and conditions, but is also easily extensible and allows model specific "
                "actions/conditions.",
    long_description=description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-polymorphic>=1.1',
    ],
    test_suite='runtests.run_tests',
    tests_require=[
        'factory_boy>=2.8.1',
        'freezegun>=0.3.8',
    ],
    keywords='django conditions ifttt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
