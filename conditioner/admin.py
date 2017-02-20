"""
Conditioner module Django Admin integration
"""
from django.contrib import admin
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.contenttypes.models import ContentType

from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline

from conditioner.actions import SendTemplatedEmailAction, LoggerAction
from conditioner.actions.forms import SendTemplatedEmailActionModelForm
from conditioner.base import BaseAction, BaseCondition
from conditioner.conditions import DayOfMonthCondition, DayOfWeekCondition, ModelSignalCondition
from conditioner.models import Rule


class ActionInline(StackedPolymorphicInline):
    """
    An inline for `conditioner.base.BaseAction` polymorphic model

    By default allows default, already implemented actions but can be easily extended by adding
    `StackedPolymorphicInline.Child` classes with custom action models to 'child_inlines'
    """
    class SendTemplatedEmailActionInline(StackedPolymorphicInline.Child):
        model = SendTemplatedEmailAction
        form = SendTemplatedEmailActionModelForm

    class LoggerActionInline(StackedPolymorphicInline.Child):
        model = LoggerAction

    model = BaseAction
    child_inlines = [
        SendTemplatedEmailActionInline,
        LoggerActionInline,
    ]

    def get_formset_children(self, request, obj=None):
        """
        Extends default `get_formset_children()` behavior and filters available inline choices based on
        rule's `target_content_type` (if action `model_specific()` is specified).
        """
        formset_children = list()
        for child_inline in self.child_inline_instances:
            model_specific = child_inline.model.model_specific()

            # If rule has no target model and no model specific conditions should be visible
            if obj and not obj.target_model and model_specific:
                continue

            # If rule has a target model only those with matching model (or `True`, as it requires any model)
            # should be visible
            if (obj and obj.target_model and model_specific
                    and model_specific is not True
                    and model_specific is not obj.target_model):
                continue

            formset_children.append(child_inline.get_formset_child(request, obj=obj))

        return formset_children


class ConditionInline(StackedPolymorphicInline):
    """
    An inline for `conditioner.base.BaseCondition` polymorphic model

    By default allows default, already implemented conditions but can be easily extended by adding
    `StackedPolymorphicInline.Child` classes with custom conditions models to 'child_inlines'
    """
    class DayOfMonthConditionInline(StackedPolymorphicInline.Child):
        model = DayOfMonthCondition

    class DayOfWeekConditionInline(StackedPolymorphicInline.Child):
        model = DayOfWeekCondition

    class ModelSignalConditionInline(StackedPolymorphicInline.Child):
        model = ModelSignalCondition

    model = BaseCondition
    child_inlines = [
        DayOfMonthConditionInline,
        DayOfWeekConditionInline,
        ModelSignalConditionInline,
    ]

    def get_formset_children(self, request, obj=None):
        """
        Extends default `get_formset_children()` behavior and filters available inline choices based on
        rule's `target_content_type` (if condition `model_specific()` is specified).
        """
        formset_children = list()
        for child_inline in self.child_inline_instances:
            model_specific = child_inline.model.model_specific()

            # If rule has no target model and no model specific conditions should be visible
            if obj and not obj.target_model and model_specific:
                continue

            # If rule has a target model only those with matching model (or `True`, as it requires any model)
            # should be visible
            if (obj and obj.target_model and model_specific
                    and model_specific is not True
                    and model_specific is not obj.target_model):
                continue

            formset_children.append(child_inline.get_formset_child(request, obj=obj))

        return formset_children


@admin.register(Rule)
class RuleAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    """
    Django Admin integration for `conditioner.Rule`model

    The 'action' and 'condition' relations are polymorphic, so we need `PolymorphicInlineSupportMixin` to make sure
    that inlines forms are properly handled
    """
    list_display = ('pk', 'target_content_type', 'action', 'condition', 'created', 'modified')

    def add_view(self, request, form_url='', extra_context=None):
        """
        Extends Django's default `add_view()` method and shows only 'target_content_type' field.Done that way to
        filter actions and conditions based on selected target content type (if they are model specific).
        """
        self.inlines = ()
        self.readonly_fields = ()
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Extends Django's default `add_view()` method, makes 'target_content_type' field readonly and adds inlines
        forms for rule action and condition. Done that way to filter actions and conditions based on selected
        target content type (if they are model specific).
        """
        self.inlines = (ActionInline, ConditionInline)
        self.readonly_fields = ('target_content_type',)
        return super().change_view(request, object_id, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Extends Django's default `response_add()` method and make 'Save' button act like 'Save and continue editing'.
        Done that way because create view doesn't show action and condition inline forms (change view does).
        Based on `django.contrib.auth.admin.UserAdmin.response_add()`
        """
        # The Save' button should behave like the 'Save and continue editing' button to allow adding actions and
        # conditions that are model related, except in two scenarios:
        #   - The user has pressed the 'Save and add another' button
        #   - We are adding in a popup
        if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
            request.POST['_continue'] = 1
        return super().response_add(request, obj, post_url_continue)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Extend Django's default `formfield_for_foreignkey()` method and filter available target content types.
        """
        if db_field.name == 'target_content_type':
            kwargs['queryset'] = ContentType.objects.exclude(
                # Let's avoid recursive rules for now
                app_label='conditioner'
            ).exclude(
                # Polymorphic base models shouldn't be used directly and only clutter the select list
                # To revisit in the future, as this is dependant on naming convention and thus isn't universal
                model__istartswith='base'
            ).exclude(
                # Exclude custom actions
                # As above, it's dependant on naming convention
                model__iendswith='action'
            ).exclude(
                # Exclude custom conditions
                # As above, it's dependant on naming convention
                model__iendswith='condition'
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
