from rest_framework import serializers

from core.data_access.models.location_model import Location


class GolfcourseDto(serializers.Serializer):
    locationid = serializers.IntegerField(source="locationid_id")
    numholes = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
