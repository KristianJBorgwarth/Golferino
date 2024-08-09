from rest_framework import serializers

from core.common.validators import validate_non_empty, validate_integer


class CreateGolfholeCommandSerializer(serializers.Serializer):
    golfcourseid = serializers.CharField(
        validators=[lambda value: validate_integer(value), validate_non_empty]
    )
    length = serializers.IntegerField(
        validators=[]
    )
    par = serializers.IntegerField(
        validators=[]
    )
    number = serializers.IntegerField(
        validators=[lambda value: validate_integer(value, min_value=1, max_value=18)]
    )
