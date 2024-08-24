from rest_framework import serializers


class CreateRoundDto(serializers.Serializer):
    roundid = serializers.IntegerField()
    dateplayed = serializers.CharField(max_length=255)
    golfcourseid = serializers.IntegerField(source='golfcourseid_id')
