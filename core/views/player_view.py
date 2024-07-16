from rest_framework import status, viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.serializers.player_serializer import PlayerSerializer
from core.services.player_service import PlayerService
from core.views.ResponseEnvelope import ResponseEnvelope


class PlayerView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._player_service = PlayerService()

    @swagger_auto_schema(request_body=PlayerSerializer,
                         responses={201: PlayerSerializer})
    def post(self, request):
        result = self._player_service.create_player(request.data)
        if result.is_success:
            return ResponseEnvelope.success(
                data=result.value,
                message="Player created successfully",
                status_code=result.status_code
            ).to_response()
        else:
            return ResponseEnvelope.fail(error=result.error, status_code=result.status_code).to_response()

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