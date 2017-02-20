"""
Conditioner module related exceptions
"""


class BaseConditionerException(Exception):
    """
    Base class for all conditioner related exceptions
    """
    pass


class IncorrectModelException(BaseConditionerException):
    """
    Model specific action/condition got wrong object instance
    """
    pass
