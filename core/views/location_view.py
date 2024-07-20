from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from core.commands.location.create.create_location_command import CreateLocationCommand
from core.dtos.location_dto import LocationDto
from core.queries.location.get.get_locations_query import GetLocationsQuery
from core.serializers.location.create_location_cmd_serializer import CreateLocationCommandSerializer
from core.serializers.location.get_locations_query_serializer import GetLocationsQuerySerializer
from core.setup.mediator_setup import get_mediator
from core.views.ResponseEnvelope import ResponseEnvelope


class LocationView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreateLocationCommandSerializer,
        responses={200: LocationDto, 400: 'BadRequest'}
    )
    def create(self, request):
        cmd = CreateLocationCommand(request.data.get('locationname'), request.data.get('address'), request.data.get('city'))
        result = self._mediator.send(cmd)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code).to_response()
        else:
            return ResponseEnvelope.fail(result.error, result.status_code).to_response()
        
    @swagger_auto_schema(
        query_serializer=GetLocationsQuerySerializer,
        responses={200: LocationDto(many=True), 204: 'No Content', 400: 'BadRequest'}
    )
    def get_all(self, request):
        query = GetLocationsQuery(int(request.query_params.get('page', 1)), int(request.query_params.get('page_size', 10)))

        result = self._mediator.send(query)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code).to_response()
        else:
            return ResponseEnvelope.fail(result.error, result.status_code).to_response()
