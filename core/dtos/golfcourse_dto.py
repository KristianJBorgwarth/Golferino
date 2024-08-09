from rest_framework import serializers

from core.data_access.models.location_model import Location


class GolfcourseDto(serializers.Serializer):
    locationid = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    numholes = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
