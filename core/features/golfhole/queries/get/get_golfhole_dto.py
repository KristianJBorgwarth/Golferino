from rest_framework import serializers


class GetGolfholeDto(serializers.Serializer):
    golfcourseid = serializers.IntegerField(source="golfcourseid_id")
    length = serializers.IntegerField()
    par = serializers.IntegerField()
    number = serializers.IntegerField()

