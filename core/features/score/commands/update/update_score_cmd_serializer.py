from rest_framework import serializers

from core.common.validators import validate_integer, validate_non_empty


class UpdateScoreCommandSerializer(serializers.Serializer):
    scoreid = serializers.IntegerField(
        validators=[lambda value: validate_integer(value), validate_non_empty]
    )
    strokes = serializers.IntegerField(
        validators=[lambda value: validate_integer(value, min_value=1, max_value=50), validate_non_empty]
    )
