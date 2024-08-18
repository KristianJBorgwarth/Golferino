from rest_framework import serializers


class CreateScoreDto(serializers.Serializer):
    playerroundid = serializers.IntegerField(source="playerroundid_id")
    golfholeid = serializers.IntegerField(source="golfholeid_id")
    strokes = serializers.IntegerField()
