from rest_framework import status, viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.commands.player.create.create_player_command import CreatePlayerCommand
from core.dtos.player_dto import PlayerDto
from core.queries.player.get.get_players_query import GetPlayersQuery
from core.serializers.player.create_player_cmd_serializer import CreatePlayerCommandSerializer
from core.serializers.player.get_players_query_serializer import GetPlayersQuerySerializer
from core.setup.mediator_setup import get_mediator
from core.views.ResponseEnvelope import ResponseEnvelope


class PlayerView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreatePlayerCommandSerializer,
        responses={200: PlayerDto, 400: 'BadRequest'}
    )
    def create(self, request):
        cmd = CreatePlayerCommand(request.data.get('firstname'),
                                  request.data.get('lastname'),
                                  request.data.get('email'))
        result = self._mediator.send(cmd)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)

    @swagger_auto_schema(
        query_serializer=GetPlayersQuerySerializer,
        responses={200: PlayerDto(many=True), 204: 'No Content', 400: 'BadRequest'}
    )
    def get_all(self, request):
        query = GetPlayersQuery(int(request.query_params.get('page', 1)),
                                int(request.query_params.get('page_size', 10)))

        result = self._mediator.send(query)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)
