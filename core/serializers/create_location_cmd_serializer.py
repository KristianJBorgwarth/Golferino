from rest_framework import serializers

from core.common.validators import validate_non_empty, validate_alpha, validate_min_length


class CreateLocationCommandSerializer(serializers.Serializer):
    locationname = serializers.CharField(
        max_length=255,
        validators=[validate_non_empty, validate_alpha]
    )
    address = serializers.CharField(
        max_length=1024,
        validators=[validate_non_empty, lambda value: validate_min_length(value, 5)]
    )
    city = serializers.CharField(
        max_length=255,
        validators=[validate_non_empty, validate_alpha]
    )