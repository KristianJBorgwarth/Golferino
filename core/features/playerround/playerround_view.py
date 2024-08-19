from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from core.features.playerround.commands.create.create_playerround_command import CreatePlayerroundCommand
from core.dtos.playerround_dto import PlayerroundDto
from core.features.playerround.queries.get.get_playerrounds_query import GetPlayerroundsQuery
from core.features.playerround.commands.create.create_playerround_cmd_serializer import CreatePlayerroundCommandSerializer
from core.features.playerround.queries.get.get_playerrounds_query_serializer import GetPlayerroundsQuerySerializer
from core.setup.mediator_setup import get_mediator
from core.common.ResponseEnvelope import ResponseEnvelope


class PlayerroundView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreatePlayerroundCommandSerializer,
        responses={200: PlayerroundDto, 400: 'BadRequest'}
    )
    def create(self, request):
        cmd = CreatePlayerroundCommand(request.data.get('playerid'),
                                       request.data.get('roundid'),
                                       )
        result = self._mediator.send(cmd)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)

    @swagger_auto_schema(
        query_serializer=GetPlayerroundsQuerySerializer,
        responses={200: PlayerroundDto(many=True), 204: 'No Content', 400: 'BadRequest'}
    )
    def get_all(self, request):
        query = GetPlayerroundsQuery(page=int(request.query_params.get('page', 1)),
                                     page_size=int(request.query_params.get('page_size', 10)),
                                     playerid=int(request.query_params.get('playerid'))
                                     )

        result = self._mediator.send(query)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)