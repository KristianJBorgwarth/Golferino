from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from core.features.golfcourse.commands.create.create_golfcourse_command import CreateGolfcourseCommand
from core.dtos.golfcourse_dto import GolfcourseDto
from core.features.golfcourse.queries.get.get_golfcourses_query import GetGolfcoursesQuery
from core.features.golfcourse.commands.create.create_golfcourse_cmd_serializer import CreateGolfcourseCommandSerializer
from core.features.golfcourse.queries.get.get_golfcourses_query_serializer import GetGolfcoursesQuerySerializer
from core.setup.mediator_setup import get_mediator
from core.common.ResponseEnvelope import ResponseEnvelope


class GolfcourseView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreateGolfcourseCommandSerializer,
        responses={200: GolfcourseDto, 400: 'BadRequest'}
    )
    def create(self, request):
        cmd = CreateGolfcourseCommand(request.data.get('locationid'),
                                      request.data.get('numholes'),
                                      request.data.get('name'))
        result = self._mediator.send(cmd)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)

    @swagger_auto_schema(
        query_serializer=GetGolfcoursesQuerySerializer,
        responses={200: GolfcourseDto(many=True), 204: 'No Content', 400: 'BadRequest'}
    )
    def get_all(self, request):
        query = GetGolfcoursesQuery(int(request.query_params.get('page', 1)),
                                    int(request.query_params.get('page_size', 10)))

        result = self._mediator.send(query)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)