"""
Date related conditions models
"""
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from conditioner.base import BaseCronCondition


class DayOfMonthCondition(BaseCronCondition):
    """
    Class representation of a day of month condition

    It allows for date based conditions like 'every first day of the month'.
    """
    day = models.PositiveSmallIntegerField(
        verbose_name='day of the month',
        validators=[MaxValueValidator(31)],
        help_text="Action will occur every month on that day.",
    )

    class Meta(BaseCronCondition.Meta):
        verbose_name = 'day of month condition'
        verbose_name_plural = 'day of month conditions'

    def is_met(self, *args, **kwargs):
        """
        Condition is met when current date day is equal to `value` and `last_executed` isn't today
        """
        today = timezone.now().date()
        if self.day == today.day and (not self.last_executed or self.last_executed.date() != today):
            return True

        return False

    def __str__(self):
        return 'Day of month condition (day: {0.day})'.format(self)


class DayOfWeekCondition(BaseCronCondition):
    """
    Class representation of a day of week condition

    It allows for date based conditions like 'every Monday'.
    """
    # Based on ISO weekdays values
    WEEKDAY_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Sunday'),
        (7, 'Saturday'),
    )
    weekday = models.PositiveSmallIntegerField(
        verbose_name='day of the week',
        choices=WEEKDAY_CHOICES,
        help_text="Action will occur every week on that day.",
    )

    class Meta(BaseCronCondition.Meta):
        verbose_name = 'day of week condition'
        verbose_name_plural = 'day of week conditions'

    def is_met(self, *args, **kwargs):
        """
        Condition is met when current date week day is equal to `day` and `last_executed` isn't today
        """
        today = timezone.now().date()
        if self.weekday == today.isoweekday() and (not self.last_executed or self.last_executed.date() != today):
            return True

        return False

    def __str__(self):
        return 'Day of week condition (day: {0})'.format(self.get_weekday_display())
