from rest_framework import serializers


class RoundDto(serializers.Serializer):
    dateplayed = serializers.CharField(max_length=255)
    golfcourseid = serializers.CharField(max_length=1024)
