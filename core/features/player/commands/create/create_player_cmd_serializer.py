from rest_framework import serializers
from core.data_access.models.player_model import Player
from core.common.validators import validate_format, validate_alpha, validate_non_empty, validate_max_length, \
    validate_min_length, validate_password_format

class CreatePlayerCommandSerializer(serializers.Serializer):
    firstname = serializers.CharField(
        validators=[
            lambda value: validate_non_empty(value),
            lambda value: validate_alpha(value),
            lambda value: validate_min_length(value, 2),
            lambda value: validate_max_length(value,  20)
        ]
    )

    lastname = serializers.CharField(
        validators=[
            lambda value: validate_non_empty(value),
            lambda value: validate_alpha(value),
            lambda value: validate_min_length(value, 3),
            lambda value: validate_max_length(value, 20)
        ]
    )

    email = serializers.CharField(
        validators=[
            lambda value: validate_non_empty(value),
            lambda value: validate_format(value)
        ]
    )
    
    password = serializers.CharField(
        validators=[lambda value: validate_non_empty(value), 
                    lambda value: validate_min_length(value, 8), 
                    lambda value: validate_max_length(value, 255), 
                    lambda value: validate_password_format(value)])

    class Meta:
        model = Player
        fields = ['firstname', 'lastname', 'email', 'playerid', 'password']
        read_only_fields = ['playerid']
