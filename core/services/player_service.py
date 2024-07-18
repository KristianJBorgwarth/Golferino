from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.player_model import Player
from core.data_access.repositories.player_repository import PlayerRepository
from core.serializers.player_serializer import PlayerSerializer
from rest_framework import status


class PlayerService:
    def __init__(self):
        self._pr = PlayerRepository(Player)

    # TODO: Remove this as it has been moved into CreatePlayerCommand
    def create_player(self, data):
        if self._pr.email_exists(data['email']):
            return Result.fail(ErrorMessage.unspecified_error("Email already exists"),
                               status_code=status.HTTP_400_BAD_REQUEST)

        serializer = PlayerSerializer(data=data)
        if serializer.is_valid():
            self._pr.create(serializer.data)
            return Result.ok(serializer.data, status_code=status.HTTP_201_CREATED)
        return Result.fail(serializer.errors)

    def get_player_by_id(self, playerid):
        if not playerid.isnumeric():
            return Result.fail(ErrorMessage.unspecified_error("playerid must be an integer"),
                               status_code=status.HTTP_400_BAD_REQUEST)

        if self._pr.player_exists(playerid=playerid):
            player = self._pr.get_by_key(playerid=playerid)
            return Result.ok(PlayerSerializer(player).data, status_code=status.HTTP_200_OK)

        return Result.fail(ErrorMessage.not_found("Player not found"), status_code=status.HTTP_204_NO_CONTENT)

    def get_player_by_name(self, firstname):
        if not isinstance(firstname, str) or firstname.isnumeric():
            return Result.fail(ErrorMessage.not_found("firstname must be a string"),
                               status_code=status.HTTP_400_BAD_REQUEST)
        if self._pr.player_exists(firstname=firstname):
            player = self._pr.get_by_key(firstname=firstname)
            return Result.ok(PlayerSerializer(player).data, status_code=status.HTTP_200_OK)

        return Result.fail(ErrorMessage.not_found("Player not found"), status_code=status.HTTP_204_NO_CONTENT)