from rest_framework import serializers


class GolfcourseDto(serializers.Serializer):
    locationid = serializers.IntegerField()
    numholes = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
