from rest_framework import serializers


class CreatePlayerDto(serializers.Serializer):
    playerid = serializers.IntegerField()
    firstname = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=1024)
    email = serializers.CharField(max_length=255)
    