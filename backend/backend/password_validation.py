import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordLengthValidation:
    def __init__(self, min_length=6, max_length=20):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password must contain at least 6 characters."),
                code='password_too_short',
                params={
                    'min_length': self.min_length
                },
            )

        if len(password) > self.max_length:
            raise ValidationError(
                _("This password must contain no more than 20 characters."),
                code='password_too_long',
                params={
                    'max_length': self.max_length
                },
            )

    def get_help_text(self):
        return _(
            "Your password must contain from 6 to 20 characters."
            % {
                'min_length': self.min_length,
                'max_length': self.max_length
            }
        )


class PasswordUppercaseValidation:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class PasswordLowercaseValidation:
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )


class PasswordDigitValidation:
    def validate(self, password, user=None):
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_no_digit',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )
