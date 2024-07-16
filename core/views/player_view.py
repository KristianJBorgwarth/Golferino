from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.serializers.player_serializer import PlayerSerializer
from core.services.player_service import PlayerService
from core.views.ResponseEnvelope import ResponseEnvelope


class PlayerView(APIView):

    @swagger_auto_schema(request_body=PlayerSerializer,
                         responses={201: PlayerSerializer})
    def post(self, request):
        result = PlayerService.create_player(request.data)
        if result.is_success:
            return ResponseEnvelope.success(
                data=PlayerSerializer(result.value).data,
                message="Player created successfully",
                status_code=status.HTTP_201_CREATED
            ).to_response()
        else:
            return ResponseEnvelope.fail(
                error=result.error,
                status_code=status.HTTP_400_BAD_REQUEST
            ).to_response()

