from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models.player_model import Player
from .serializers import PlayerSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class PlayerView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Name of the player", type=openapi.TYPE_STRING)
        ],
        responses={200: PlayerSerializer(many=True)}
    )
    def get(self, request, pk=None):
        if pk:
            try:
                player = Player.objects.get(pk=pk)
            except Player.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        else:
            players = Player.objects.all()
            serializer = PlayerSerializer(players, many=True)
            return Response(serializer.data)
