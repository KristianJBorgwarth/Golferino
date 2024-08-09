from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from core.commands.golfhole.create.create_golfhole_command import CreateGolfholeCommand
from core.dtos.golfcourse_dto import GolfcourseDto
from core.serializers.golfhole.create_golfhole_cmd_serializer import CreateGolfholeCommandSerializer
from core.setup.mediator_setup import get_mediator
from core.views.ResponseEnvelope import ResponseEnvelope


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
