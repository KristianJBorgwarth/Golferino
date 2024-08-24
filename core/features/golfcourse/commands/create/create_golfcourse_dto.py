from rest_framework import serializers


class CreateGolfcourseDto(serializers.Serializer):
    golfcourseid = serializers.IntegerField()
    locationid = serializers.IntegerField(source="locationid_id")
    numholes = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
