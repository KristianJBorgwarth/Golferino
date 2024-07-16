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
            return Result.fail(ErrorMessage.unspecified_error("Email already exists"),
                               status_code=status.HTTP_400_BAD_REQUEST)

        serializer = PlayerSerializer(data=data)
        if serializer.is_valid():
            player = serializer.save()
            return Result.ok(PlayerSerializer(player).data)
        return Result.fail(serializer.errors)

    @staticmethod
    def get_player_by_id(playerid):
        if not playerid.isnumeric():
            return Result.fail(ErrorMessage.unspecified_error("playerid must be an integer"),
                               status_code=status.HTTP_400_BAD_REQUEST)
        try:
            player = Player.objects.get(playerid=playerid)
            return Result.ok(PlayerSerializer(player).data, status_code=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Result.fail(ErrorMessage.not_found("Player not found"), status_code=status.HTTP_204_NO_CONTENT)


    @staticmethod
    def get_player_by_name(firstname):
        if not isinstance(firstname, str) or firstname.isnumeric():
            return Result.fail(ErrorMessage.not_found("firstname must be a string"),
                               status_code=status.HTTP_400_BAD_REQUEST)
        try:
            player = Player.objects.get(firstname=firstname)
            return Result.ok(PlayerSerializer(player).data, status_code=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Result.fail(ErrorMessage.not_found("Player not found"), status_code=status.HTTP_204_NO_CONTENT)