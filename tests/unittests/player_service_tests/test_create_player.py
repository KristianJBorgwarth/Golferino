import os
import unittest
from unittest.mock import patch, MagicMock

import django
from django.db import connection

from core.common.error_messages import ErrorMessage

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from django.test import TestCase
from django.core.management import call_command
from rest_framework import status, serializers
from core.data_access.models.player_model import Player

from core.serializers.player_serializer import PlayerSerializer
from core.services.player_service import PlayerService


class TestPlayerService(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Disable foreign key checks
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = OFF;')
        # Ensure migrations are applied before tests
        call_command('migrate')
        # Re-enable foreign key checks
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')

    @patch('core.data_access.repositories.player_repository.PlayerRepository.email_exists')
    @patch('core.serializers.player_serializer.PlayerSerializer.save')
    @patch('core.serializers.player_serializer.PlayerSerializer.is_valid')
    def test_create_player_email_exists(self, mock_is_valid, mock_save, mock_email_exists):
        # Mock the email_exists to simulate email already exists
        mock_email_exists.return_value = True
        mock_is_valid.return_value = True

        # Call the service method
        data = {
            'firstname': 'testFirstName',
            'lastname': 'testLastName',
            'email': 'test@example.com'
        }
        result = PlayerService().create_player(data)

        # Assertions
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, "Email already exists")
        mock_email_exists.assert_called_once_with(data['email'])
        mock_save.assert_not_called()

    def test_create_player_success(self):
        data = {
            'firstname': 'testFirst',
            'lastname': 'testLast',
            'email': 'test2@example.com'
        }
        result = PlayerService().create_player(data)

        # Assertions
        self.assertTrue(result.is_success)
        self.assertEqual(result.value['firstname'], 'testFirst')
        self.assertEqual(result.value['lastname'], 'testLast')
        self.assertEqual(result.value['email'], 'test2@example.com')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Verify the player was actually created in the database
        player = Player.objects.get(email='test2@example.com')
        self.assertIsNotNone(player)
        self.assertEqual(player.firstname, 'testFirst')
        self.assertEqual(player.lastname, 'testLast')

    @patch('core.data_access.repositories.player_repository.PlayerRepository.email_exists')
    @patch('core.serializers.player_serializer.PlayerSerializer.save')
    @patch('core.serializers.player_serializer.PlayerSerializer.is_valid')
    def test_create_player_invalid_data(self, mock_is_valid, mock_save, mock_email_exists):
        # Mock the email_exists to simulate email does not exist
        mock_email_exists.return_value = False
        mock_is_valid.return_value = False
        mock_errors = {'email': ['This field is required.']}
        mock_is_valid.errors = mock_errors

        # Call the service method
        data = {
            'firstname': 'testFirstName',
            'lastname': 'testLastName',
            'email': 'test@example.com'
        }
        result = PlayerService().create_player(data)

        # Assertions
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, mock_errors)
        mock_email_exists.assert_called_once_with(data['email'])
        mock_save.assert_not_called()


if __name__ == '__main__':
    unittest.main()