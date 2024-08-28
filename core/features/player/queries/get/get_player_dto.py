from rest_framework import serializers


class GetPlayerDto(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=1024)
    email = serializers.CharField(max_length=255)
