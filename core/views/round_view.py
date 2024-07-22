from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema

from core.commands.round.create.create_round_command import CreateRoundCommand
from core.dtos.round_dto import RoundDto
from core.serializers.round.create_round_cmd_serializer import CreateRoundCommandSerializer
from core.setup.mediator_setup import get_mediator
from core.views.ResponseEnvelope import ResponseEnvelope


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
            print(result.status_code)
            return ResponseEnvelope.success(result.value, int(result.status_code))
        else:
            print(result.status_code)
            return ResponseEnvelope.fail(result.error, int(result.status_code))
