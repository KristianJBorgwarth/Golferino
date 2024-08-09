from rest_framework import serializers

from core.common.validators import validate_non_empty, validate_integer
from core.data_access.models.location_model import Location


class CreateGolfcourseCommandSerializer(serializers.Serializer):
    locationid = serializers.CharField(
        validators=[lambda value: validate_integer(value), validate_non_empty]
    )
    numholes = serializers.IntegerField(
        validators=[validate_non_empty, lambda value: validate_integer(value=value, min_value=1, max_value=18)]
    )
    name = serializers.CharField(
        max_length=100,
        validators=[validate_non_empty]
    )