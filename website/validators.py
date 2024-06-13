from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_custom_email(value):
    # Regular expression to match the required pattern
    pattern = r'^(?=.[a-z])(?=.*\d).+$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Invalid email ID. Must enter upper case, numbers.'),
            params={'value': value},
        )
# def validate_mobile_number(value):
#     pattern = r'^[6-9]\d{9}$'
#     if not re.match(pattern, value):
#         raise ValidationError(
#             _('Invalid mobile number. It must start with a digit between 6 and 9 and be 10 digits long.'),
#             params={'value': value},
#         )








def validate_mobile_number(value):
    pattern = r'^\+91[-\s]?[6-9]\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Invalid mobile number. It must include the country code +91 and be 10 digits long.'),
            params={'value': value},
        )
