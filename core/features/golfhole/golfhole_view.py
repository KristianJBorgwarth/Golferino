from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from core.features.golfhole.commands.create.create_golfhole_command import CreateGolfholeCommand
from core.dtos.golfcourse_dto import GolfcourseDto
from core.features.golfhole.commands.create.create_golfhole_cmd_serializer import CreateGolfholeCommandSerializer
from core.features.golfhole.queries.get.get_golfhole_dto import GetGolfholeDto
from core.features.golfhole.queries.get.get_golfholes_query import GetGolfholesQuery
from core.features.golfhole.queries.get.get_golfholes_query_serializer import GetGolfholesQuerySerializer
from core.setup.mediator_setup import get_mediator
from core.common.ResponseEnvelope import ResponseEnvelope


class GolfholeView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreateGolfholeCommandSerializer,
        responses={200: GolfcourseDto, 400: 'BadRequest'}
    )
    def create(self, request):
        print(request.data.get("golfcourseid"))
        cmd = CreateGolfholeCommand(request.data.get('golfcourseid'),
                                      request.data.get('length'),
                                      request.data.get('par'),
                                      request.data.get('number'))
        result = self._mediator.send(cmd)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)

    @swagger_auto_schema(
        query_serializer=GetGolfholesQuerySerializer,
        responses={200: GetGolfholeDto(many=True), 204: 'No Content', 400: 'BadRequest'}
    )
    def get_all(self, request):
        query = GetGolfholesQuery(int(request.query_params.get('page', 1)),
                                  int(request.query_params.get('page_size', 10)))

        result = self._mediator.send(query)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)
