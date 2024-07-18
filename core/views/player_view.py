from rest_framework import status, viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.commands.player.create.create_player_command import CreatePlayerCommand
from core.dtos.player_dto import PlayerDto
from core.serializers.player.create_player_cmd_serializer import CreatePlayerCommandSerializer
from core.serializers.player_serializer import PlayerSerializer
from core.services.player_service import PlayerService
from core.setup.mediator_setup import get_mediator
from core.views.ResponseEnvelope import ResponseEnvelope


class PlayerView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._player_service = PlayerService()
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
            return ResponseEnvelope.success(result.value, result.status_code).to_response()
        else:
            return ResponseEnvelope.fail(result.error, result.status_code).to_response()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('playerid', openapi.IN_QUERY, description="Player ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: PlayerSerializer,
            400: openapi.Response('Bad Request', examples={'application/json': {'detail': 'Invalid input'}}),
            404: openapi.Response('Not Found', examples={'application/json': {'detail': 'Not found'}}),
        }
    )
    @action(methods=["get"], detail=False, url_path="get_by_id")
    def get_by_id(self, request):
        playerid = request.query_params.get('playerid')

        result = PlayerService().get_player_by_id(playerid=playerid)
        if result.is_success:
            return ResponseEnvelope.success(
                data=PlayerSerializer(result.value).data,
                status_code=result.status_code
            ).to_response()
        else:
            return ResponseEnvelope.fail(
                error=result.error,
                status_code=result.status_code
            ).to_response()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('firstname', openapi.IN_QUERY, description="Player Name", type=openapi.TYPE_STRING)
        ],
        responses={
            200: PlayerSerializer,
            400: openapi.Response('Bad Request', examples={'application/json': {'detail': 'Invalid input'}}),
            404: openapi.Response('Not Found', examples={'application/json': {'detail': 'Not found'}}),
        }
    )
    @action(methods=["get"], detail=False, url_path="get_by_name")
    def get_by_name(self, request):
        firstname = request.query_params.get('firstname')

        result = PlayerService().get_player_by_name(firstname=firstname)
        if result.is_success:
            return ResponseEnvelope.success(
                data=PlayerSerializer(result.value).data,
                status_code=result.status_code
            ).to_response()
        else:
            return ResponseEnvelope.fail(
                error=result.error,
                status_code=result.status_code
            ).to_response()
