import os

import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from core.models.player_model import Player
from core.serializers.player_serializer import PlayerSerializer
from core.common.results import Result
from core.common.error_messages import ErrorMessage

class PlayerViewTests(APITestCase):

    @patch('core.services.player_service.PlayerService.get_player_by_id')
    def test_get_by_id_success(self, mock_get_player_by_id):
        player = Player(firstname="John", lastname="Doe", email="john.doe@example.com")
        serializer = PlayerSerializer(player)
        mock_get_player_by_id.return_value = Result.ok(player)

        url = reverse('player-by-id')
        response = self.client.get(url, {'playerid': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], serializer.data)
        self.assertTrue(response.data['success'])
        self.assertIsNone(response.data['error'])

    @patch('core.services.player_service.PlayerService.get_player_by_id')
    def test_get_by_id_not_found(self, mock_get_player_by_id):
        mock_get_player_by_id.return_value = Result.fail(ErrorMessage.not_found("Player not found"),
                                                         status_code=status.HTTP_404_NOT_FOUND)

        url = reverse('player-by-id')
        response = self.client.get(url, {'playerid': 999})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error'], "Player not found")

    @patch('core.services.player_service.PlayerService.get_player_by_name')
    def test_get_by_name_success(self, mock_get_player_by_name):
        player = Player(firstname="John", lastname="Doe", email="john.doe@example.com")
        serializer = PlayerSerializer(player)
        mock_get_player_by_name.return_value = Result.ok(player)

        url = reverse('player-by-name')
        response = self.client.get(url, {'firstname': 'John'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], serializer.data)
        self.assertTrue(response.data['success'])
        self.assertIsNone(response.data['error'])

    @patch('core.services.player_service.PlayerService.get_player_by_name')
    def test_get_by_name_not_found(self, mock_get_player_by_name):
        mock_get_player_by_name.return_value = Result.fail(ErrorMessage.not_found("Player not found"),
                                                           status_code=status.HTTP_404_NOT_FOUND)

        url = reverse('player-by-name')
        response = self.client.get(url, {'firstname': 'Unknown'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error'], "Player not found")
