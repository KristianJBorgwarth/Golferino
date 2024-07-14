from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.models.player_model import Player
from core.serializers.player_serializer import PlayerSerializer
from rest_framework import status
from rest_framework.response import Response


class PlayerService:

    @staticmethod
    def create_player(data):
        if Player.objects.filter(email=data['email']).exists():
            return Result.fail(ErrorMessage.unspecified_error("Email already exists"))

        serializer = PlayerSerializer(data=data)
        if serializer.is_valid():
            player = serializer.save()
            return Result.ok(PlayerSerializer(player).data)
        return Result.fail(serializer.errors)
