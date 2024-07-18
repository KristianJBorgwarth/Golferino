from rest_framework import serializers


class LocationDto(serializers.Serializer):
    locationname = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=1024)
    city = serializers.CharField(max_length=255)
