from rest_framework import serializers

from core.common.validators import validate_non_empty, validate_integer
from core.data_access.models.playerround_model import Playerround


class UpdatePlayerroundCommandSerializer(serializers.Serializer):
    playerroundid = serializers.CharField(
        validators=[lambda value: validate_integer(value), validate_non_empty]
    )

    class Meta:
        model = Playerround
        fields = ['roundid', 'totalscore']
        read_only_fields = ['playerid', 'roundid']