from django.core.management.base import BaseCommand
from django.utils import timezone

from conditioner.base import BaseCronCondition


class Command(BaseCommand):
    help = "Check cron related conditions and run their actions if the condition is met"

    def handle(self, *args, **options):
        conditions = BaseCronCondition.objects.exclude(rule__isnull=True)

        for condition in conditions:
            # Make sure that there is an action to be run
            if not hasattr(condition.rule, 'action'):
                self.stdout.write(self.style.WARNING(
                    "Condition was met but rule {} doesn't have linked action.".format(condition.rule.pk))
                )
                continue

            # Generic conditions
            if condition.model_specific() is False:
                if condition.is_met():
                    condition.rule.action.run_action()
                    condition.last_executed = timezone.now()
                    condition.save()

                    self.stdout.write(self.style.SUCCESS(
                        "Condition for rule {} was met and the action "
                        "was successfully executed".format(condition.rule.pk))
                    )
            # Model specific conditions
            else:
                for instance in condition.rule.target_model.objects.all():
                    if condition.is_met(instance):
                        condition.rule.action.run_action(instance)
                        condition.last_executed = timezone.now()
                        condition.save()

                        self.stdout.write(self.style.SUCCESS(
                            "Model specific condition for rule {} was met and the action "
                            "was successfully executed".format(condition.rule.pk))
                        )

        self.stdout.write(self.style.SUCCESS("\nAll done!"))
