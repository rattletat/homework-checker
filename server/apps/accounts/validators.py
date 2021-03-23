from django.core.exceptions import ValidationError

import re


class _ValidatorBase:
    __slots__ = ("message",)
    DEFAULT_MSG = ""

    def __init__(self, message=None):
        self.message = message if message else self.DEFAULT_MSG

    def get_help_text(self):
        return self.message

    def validate(self, *args, **kwargs):
        raise NotImplementedError()


class HasLowerCaseValidator(_ValidatorBase):
    __slots__ = ()
    DEFAULT_MSG = "The password must contain at least one lowercase character."

    def validate(self, password, user=None):
        if re.search("[a-z]", password) is None:
            raise ValidationError(self.message, code="missing_lower_case")


class HasUpperCaseValidator(_ValidatorBase):
    __slots__ = ()
    DEFAULT_MSG = "The password must contain at least one uppercase character."

    def validate(self, password, user=None):
        if re.search("[A-Z]", password) is None:
            raise ValidationError(self.message, code="missing_upper_case")


class HasNumberValidator(_ValidatorBase):
    __slots__ = ()
    DEFAULT_MSG = "The password must contain at least one numeric character."

    def validate(self, password, user=None):
        if re.search("[0-9]", password) is None:
            raise ValidationError(self.message, code="missing_numeric")
