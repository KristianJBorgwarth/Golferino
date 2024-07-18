from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet

from core.commands.location.create.create_location_command import CreateLocationCommand
from core.dtos.location_dto import LocationDto
from core.serializers.create_location_cmd_serializer import CreateLocationCommandSerializer
from core.setup.mediator_setup import get_mediator
from core.views.ResponseEnvelope import ResponseEnvelope


class LocationView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreateLocationCommandSerializer,
        responses={201: LocationDto, 400: 'Invalid input'}
    )
    def create(self, request):
        cmd = CreateLocationCommand(request.data.get('locationname'), request.data.get('address'), request.data.get('city'))
        result = self._mediator.send(cmd)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code).to_response()
        else:
            return ResponseEnvelope.fail(result.error, result.status_code).to_response()
