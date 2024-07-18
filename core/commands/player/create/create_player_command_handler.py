from abc import ABC

from rest_framework import status

from core.commands.player.create.create_player_command import CreatePlayerCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.player_model import Player
from core.common.mediator import RequestHandler
from core.data_access.repositories.player_repository import PlayerRepository
from core.dtos.player_dto import PlayerDto
from core.serializers.player.create_player_cmd_serializer import CreatePlayerCommandSerializer


class CreatePlayerCommandHandler(RequestHandler[CreatePlayerCommand, Result[PlayerDto]]):
    def __init__(self):
        self.player_repository = PlayerRepository(Player)

    def handle(self, command: CreatePlayerCommand) -> Result[PlayerDto]:
        serializer = CreatePlayerCommandSerializer(
            data={
            'firstname': command.firstname,
            'lastname': command.lastname,
            'email': command.email
        })

        if not serializer.is_valid():
            return Result.fail(serializer.errors, status_code=400)

        player_data = serializer.validated_data

        if self.player_repository.player_exists(email=player_data['email']):
            return Result.fail(ErrorMessage.already_exists(player_data['email']), status_code=400)

        player = self.player_repository.create(player_data)
        playerDto = PlayerDto(player)

        return Result.ok(playerDto.data, status_code=200)
