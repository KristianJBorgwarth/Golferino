from rest_framework import serializers

# core/serializers.py

from rest_framework import serializers
from .models.player_model import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
