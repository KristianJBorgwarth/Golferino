import os
import unittest
from unittest.mock import patch, MagicMock

import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.services.player_service import PlayerService
from core.serializers.player_serializer import PlayerSerializer


class TestPlayerService(unittest.TestCase):

    @patch('core.data_access.models.player_model.Player.objects.filter')
    @patch('core.serializers.player_serializer.PlayerSerializer.save')
    @patch('core.serializers.player_serializer.PlayerSerializer.is_valid')
    def test_create_player_email_exists(self, mock_is_valid, mock_save, mock_filter):
        # Mock the filter to simulate email already exists
        mock_filter.return_value.exists.return_value = True
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
        mock_filter.assert_called_once_with(email=data['email'])
        mock_filter.return_value.exists.assert_called_once()
        mock_save.assert_not_called()
        print("Tested error message for email already exists")
        print("Tested result.is_success = False for email already exists")

    @patch('core.data_access.models.player_model.Player.objects.filter')
    @patch('core.data_access.base_repositories.repository.Repository.create')
    @patch('core.serializers.player_serializer.PlayerSerializer.is_valid')
    @patch('core.serializers.player_serializer.PlayerSerializer.data', new_callable=MagicMock)
    def test_create_player_success(self, mock_data, mock_is_valid, mock_save, mock_filter):
        # Mock the filter to simulate email does not exist
        mock_filter.return_value.exists.return_value = False
        mock_is_valid.return_value = True
        mock_data.return_value = {
            'firstname': 'testFirstName',
            'lastname': 'testLastName',
            'email': 'test@example.com'
        }
        mock_saved_player = MagicMock()
        mock_save.return_value = mock_saved_player

        # Call the service method
        data = {
            'firstname': 'testFirstName',
            'lastname': 'testLastName',
            'email': 'test@example.com'
        }
        result = PlayerService().create_player(data)

        # Assertions
        self.assertTrue(result.is_success)
        mock_filter.assert_called_once_with(email=data['email'])
        mock_is_valid.assert_called_once()
        mock_save.assert_called_once()

    @patch('core.data_access.models.player_model.Player.objects.filter')
    @patch('core.serializers.player_serializer.PlayerSerializer.save')
    @patch('core.serializers.player_serializer.PlayerSerializer.is_valid')
    def test_create_player_invalid_data(self, mock_is_valid, mock_save, mock_filter):
        # Mock the filter to simulate email does not exist
        mock_filter.return_value.exists.return_value = False
        mock_is_valid.return_value = False
        mock_errors = {'email': ['This field is required.']}
        PlayerSerializer.errors = mock_errors

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
        mock_filter.assert_called_once_with(email=data['email'])
        mock_save.assert_not_called()


if __name__ == '__main__':
    unittest.main()