from rest_framework import serializers


class CreatePlayerDto(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=1024)
    email = serializers.CharField(max_length=255)
    