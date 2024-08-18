from rest_framework import serializers


class GetGolfcourseDto(serializers.Serializer):
    golfcourseid = serializers.IntegerField()
    locationid = serializers.IntegerField(source="locationid_id")
    numholes = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
