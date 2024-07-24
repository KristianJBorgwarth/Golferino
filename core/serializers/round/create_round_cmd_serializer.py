from rest_framework import serializers
from core.common.validators import validate_non_empty, validate_date_not_in_future, \
    validate_integer
from core.data_access.models.round_model import Round


class CreateRoundCommandSerializer(serializers.Serializer):
    dateplayed = serializers.DateField(
        validators=[validate_non_empty, validate_date_not_in_future
        ]
    )
    golfcourseid = serializers.CharField(
        validators=[
            lambda value: validate_integer(value)
        ]
    )

    class Meta:
        model = Round
        fields = ['roundid', 'golfcourseid', 'dateplayed']
        read_only_fields = ['playerid']
