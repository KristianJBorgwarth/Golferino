from rest_framework import serializers

from core.common.validators import validate_max_length, validate_min_length, validate_non_empty


class GetPlayersQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(validators=[lambda value: validate_non_empty,
                                                lambda value: validate_min_length(value, 1)], default=1)
    page_size = serializers.IntegerField(validators=[lambda value: validate_non_empty,
                                                     lambda value: validate_min_length(value,1),
                                                     lambda value: validate_max_length(value, 10)], default=1)
