"""
Conditioner module AppConfig integration
"""
from django import db
from django.apps import AppConfig


class ConditionerAppConfig(AppConfig):
    """
    Django AppConfig integration for `conditioner` module
    """
    name = 'conditioner'
    verbose_name = 'Conditioner'

    def ready(self):
        # Make sure that all models are imported
        from conditioner import actions  # noqa
        from conditioner import conditions  # noqa

        # Signals aren't persistent so we need to register them on startup
        try:
            for signal_condition in conditions.ModelSignalCondition.objects.all():
                signal_condition.connect_signal()
        except db.DatabaseError:  # Django migrations weren't run yet
            pass
