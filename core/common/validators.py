from rest_framework import serializers

from core.common.error_messages import ErrorMessage


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


def validate_format(value):
    if "@" not in value:
        raise serializers.ValidationError(ErrorMessage.must_contain_at_symbol(value, '@'))
