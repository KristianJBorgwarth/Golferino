from rest_framework import serializers


class UpdateScoreDto(serializers.Serializer):
    scoreid = serializers.IntegerField()
    strokes = serializers.IntegerField()
