from rest_framework import serializers


class GetPlayerroundDto(serializers.Serializer):
    playerroundid = serializers.IntegerField()
    roundid = serializers.IntegerField(source='roundid_id')
    playerid = serializers.IntegerField(source='playerid_id')
    totalscore = serializers.IntegerField()
