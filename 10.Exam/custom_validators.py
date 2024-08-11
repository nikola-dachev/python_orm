import re

from django.core.exceptions import ValidationError


def all_digits(value):
    if not re.match(r'^[0-9]+$', value):
        raise ValidationError('')
