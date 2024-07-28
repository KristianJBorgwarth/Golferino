from rest_framework import serializers


class PlayerroundDto(serializers.Serializer):
    playerroundid = serializers.IntegerField()
    roundid = serializers.IntegerField()
    playerid = serializers.IntegerField()
    totalscore = serializers.IntegerField()
