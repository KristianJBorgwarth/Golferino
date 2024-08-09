from rest_framework import serializers

from core.data_access.models.location_model import Location


class GolfholeDto(serializers.Serializer):
    golfcourseid = serializers.IntegerField(source="golfcourseid_id")
    length = serializers.IntegerField()
    par = serializers.IntegerField()
    number = serializers.IntegerField()

