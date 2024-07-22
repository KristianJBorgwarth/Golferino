from datetime import datetime

from rest_framework import serializers

from core.common.error_messages import ErrorMessage


def validate_date_not_in_future(value: str, dateformat: str = 'YYYYMMDD') -> bool:
    input_date = datetime.strptime(value, dateformat)
    now = datetime.now()
    return input_date < now


def validate_dateformat(value: str, dateformat: str = 'YYYYMMDD') -> bool:
    try:
        return bool(datetime.strptime(value, dateformat))
    except ValueError:
        return False


def validate_non_empty(value):
    if not value:
        raise serializers.ValidationError(ErrorMessage.value_cant_be_empty(value))


def validate_alpha(value):
    if not value.isalpha():
        raise serializers.ValidationError(ErrorMessage.must_contain_only_letters(value))


def validate_min_length(value, min_length):
    if len(value) < min_length:
        raise serializers.ValidationError(ErrorMessage.must_be_at_least(value, min_length))


def validate_max_length(value, max_length):
    if len(value) > max_length:
        raise serializers.ValidationError(ErrorMessage.must_be_less_than(value, max_length))


def validate_integer(value, min_value=None, max_value=None):
    if not isinstance(value, int):
        raise serializers.ValidationError(ErrorMessage.must_be_of_type(value, 'integer'))
    if min_value is not None and int(value) < min_value:
        raise serializers.ValidationError(ErrorMessage.must_be_at_least(value, min_value))
    if max_value is not None and int(value) > max_value:
        raise serializers.ValidationError(ErrorMessage.must_be_less_than(value, max_value))
    

def validate_format(value):
    if "@" not in value:
        raise serializers.ValidationError(ErrorMessage.must_contain_at_symbol(value, '@'))
