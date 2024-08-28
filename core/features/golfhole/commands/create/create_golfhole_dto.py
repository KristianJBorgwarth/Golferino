from rest_framework import serializers


class CreateGolfholeDto(serializers.Serializer):
    golfholeid = serializers.IntegerField()
    golfcourseid = serializers.IntegerField(source="golfcourseid_id")
    length = serializers.IntegerField()
    par = serializers.IntegerField()
    number = serializers.IntegerField()

