from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema

from core.features.round.commands.create.create_round_command import CreateRoundCommand
from core.dtos.round_dto import RoundDto
from core.features.round.commands.create.create_round_cmd_serializer import CreateRoundCommandSerializer
from core.features.round.queries.get.get_round_dto import GetRoundDto
from core.features.round.queries.get.get_rounds_query import GetRoundsQuery
from core.features.round.queries.get.get_rounds_query_serializer import GetRoundsQuerySerializer
from core.setup.mediator_setup import get_mediator
from core.common.ResponseEnvelope import ResponseEnvelope


class RoundView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreateRoundCommandSerializer,
        responses={200: RoundDto, 400: 'BadRequest'}
    )
    def create(self, request):
        cmd = CreateRoundCommand(request.data.get('golfcourseid'),
                                 request.data.get('dateplayed'))

        result = self._mediator.send(cmd)
        if result.is_success:
            return ResponseEnvelope.success(result.value, int(result.status_code))
        else:
            return ResponseEnvelope.fail(result.error, int(result.status_code))

    @swagger_auto_schema(
        query_serializer=GetRoundsQuerySerializer,
        responses={200: GetRoundDto(many=True), 204: 'No Content', 400: 'BadRequest'}
    )
    def get_all(self, request):
        query = GetRoundsQuery(int(request.query_params.get('page', 1)),
                               int(request.query_params.get('page_size', 10)))

        result = self._mediator.send(query)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)