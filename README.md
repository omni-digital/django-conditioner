# django-conditioner
[![Build status](https://img.shields.io/travis/omni-digital/django-conditioner.svg)][travis]
[![PyPI version](https://img.shields.io/pypi/v/django-conditioner.svg)][pypi]
[![Python versions](https://img.shields.io/pypi/pyversions/django-conditioner.svg)][pypi]
[![License](https://img.shields.io/github/license/omni-digital/django-conditioner.svg)][license]

Create simple 'if this then that' style rules in your Django application. Comes with a bunch of ready-to-use actions
and conditions, but is also easily extensible and allows model specific actions/conditions.

Conditioner helps you create simple rules that consist of a condition (if this), and an action (then that). It's
currently a work in progress, but we successfully use it in production with custom conditions and actions that allow us
to send 'reminder' emails to users before their license expires.

It was created to 'scratch an itch', and for the foreseeable future we will prioritise implementing use-cases needed by
us as. The overall goal, however, is to create a set of useful actions and conditions that could be applied to a number
of different scenarios.

Oh, and shout-out to [django-polymorphic][django-polymorphic] without which this whole thing would be much harder to do.

## Installation
From PyPI:

```shell
$ pip install django-conditioner
```

## Usage
If you want to use the already implemented actions and conditions then all you need to do is install the package, add
`conditioner` to your list of `INSTALLED_APPS` and run `$ python manage.py migrate`.

You should then see a `Conditioner` section with a `Rule` child in Django Admin. Adding a new one should be pretty
self-explanatory.

## Advanced usage

### Actions and conditions types
Both actions and conditions are divided into generic, model generic and model specific types:  
- generic actions/conditions don't need a set target type (i.e. log a message on every Monday)
- model generic actions/conditions need a set target type, but work with all available models (i.e. log a message when
 selected target type instance was created)
- model specific actions/conditions are implemented with specific model in mind and area available only when it's
 selected (i.e. send email to user on every Monday); they usually operate on specific fields (`user.email` in 
 previous example)

### Adding new actions and/or conditions
One of the main goals was to make conditioner as flexible as possible and make adding new actions/conditions as easy
as possible.

#### Creating the action
All actions need to inherit from `BaseAction` and implement `run_action()`. Model generic actions should set
`model_specific` to `True`, model specific actions should set it to return the needed model class. If your action is
model specific then model instance will be passed to `run_action()` method as `instance` named argument.

#### Making sure that the action is picked up by Django
You'll need to make sure that your newly created action is picked up by Django. Assuming that it lives in an
`actions.py` file inside `sample_module` module, your `sample_module/apps.py` should look something like this:

```python
from django.apps import AppConfig


class SampleModuleAppConfig(AppConfig):
    name = 'sample_module'

    def ready(self):
        # Make sure that all models are imported
        from sample_module import actions  # noqa
```

#### Registering action to Django Admin
Finally you'll need to hook up your action to the `Rule` Django Admin. You do that by adding it to the list of available
inline polymorphic models:

```python
from polymorphic.admin import StackedPolymorphicInline

from conditioner.admin import ActionInline
from sample_module.actions import SampleModuleAction


# Register `SampleModuleAction` action to 'conditioner' Django Admin
class SampleModuleActionInline(StackedPolymorphicInline.Child):
    model = SampleModuleAction


ActionInline.child_inlines.append(SampleModuleActionInline)
```

Assuming you put the code above in the `sample_module/conditioner.py` file, you'll need to make sure that it's also
picked up by Django by adding `from sample_module import conditioner` to your app config `ready()` method.

You should now see your custom action in Django Admin.

## API
There's no proper documentation as of now, but the code is commented and _should_ be pretty straightforward to use.

That said - feel free to open a [GitHub issue][github add issue] if anything is unclear.

## Tests
Package was tested with the help of `tox` on Python 3.4, 3.5 and 3.6 with Django 1.8, 1.9 and 1.10 (see `tox.ini`).

To run tests yourself you need to run `tox` inside the repository:

```shell
$ tox
```

## Contributions
Package source code is available at [GitHub][github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements, add functionality and point out any
mistakes. Thanks!

New actions and conditions more then welcome but should be first discussed and agreed upon.

## Authors
Developed and maintained by [Omni Digital][omni digital].

Released under [MIT License][license].


[django-polymorphic]: https://github.com/django-polymorphic/django-polymorphic/
[github]: https://github.com/omni-digital/django-conditioner/
[github add issue]: https://github.com/omni-digital/django-conditioner/issues/new
[license]: https://github.com/omni-digital/django-conditioner/blob/master/LICENSE
[omni digital]: https://omni-digital.co.uk/
[pypi]: https://pypi.python.org/pypi/django-conditioner
[travis]: https://travis-ci.org/omni-digital/django-conditioner
