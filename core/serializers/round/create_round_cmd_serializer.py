from rest_framework import serializers
from core.common.validators import validate_non_empty, validate_dateformat, validate_date_not_in_future
from core.data_access.models.round_model import Round


class CreateRoundCommandSerializer(serializers.Serializer):
    dateplayed = serializers.CharField(
        validators=[
            lambda value: validate_non_empty(value),
            lambda value: validate_dateformat(value),
            lambda value: validate_date_not_in_future(value)
        ]
    )

    class Meta:
        model = Round
        fields = ['roundid', 'golfcourseid', 'dateplayed']
        read_only_fields = ['playerid']
