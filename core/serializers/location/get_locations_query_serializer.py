from rest_framework import serializers

from core.common.validators import validate_integer, validate_max_length, validate_min_length, validate_non_empty


#TODO: SUGGESTION: maybe move to queries/location/getLocations directory
class GetLocationsQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(validators=[lambda value: validate_integer(value, min_value=1)], default=1)
    page_size = serializers.IntegerField(validators=[lambda value: validate_integer(value, min_value=1, max_value=10)], default=1)
