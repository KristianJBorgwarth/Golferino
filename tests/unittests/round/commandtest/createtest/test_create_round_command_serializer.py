import os
import unittest
import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from datetime import datetime, timedelta
from core.serializers.round.create_round_cmd_serializer import CreateRoundCommandSerializer


class TestCreateRoundCommandSerializer(unittest.TestCase):

    def test_serializer_with_valid_data(self):
        # Arrange
        valid_data = {
            'golfcourseid': '123',
            'dateplayed': '2023-07-22'
        }

        # Act
        serializer = CreateRoundCommandSerializer(data=valid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertTrue(is_valid)
        self.assertEqual(serializer.validated_data['golfcourseid'], '123')
        self.assertEqual(serializer.validated_data['dateplayed'], datetime.strptime('2023-07-22', '%Y-%m-%d').date())

    def test_serializer_with_missing_golfcourseid(self):
        # Arrange
        invalid_data = {
            'dateplayed': '2023-07-22'
        }

        # Act
        serializer = CreateRoundCommandSerializer(data=invalid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn('golfcourseid', serializer.errors)

    def test_serializer_with_missing_dateplayed(self):
        # Arrange
        invalid_data = {
            'golfcourseid': '123'
        }

        # Act
        serializer = CreateRoundCommandSerializer(data=invalid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn('dateplayed', serializer.errors)

    def test_serializer_with_invalid_dateplayed_format(self):
        # Arrange
        invalid_data = {
            'golfcourseid': '123',
            'dateplayed': '22-07-2023'  # Invalid format
        }

        # Act
        serializer = CreateRoundCommandSerializer(data=invalid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn('dateplayed', serializer.errors)

    def test_serializer_with_future_dateplayed(self):
        # Arrange
        future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        invalid_data = {
            'golfcourseid': '123',
            'dateplayed': future_date
        }

        # Act
        serializer = CreateRoundCommandSerializer(data=invalid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn('dateplayed', serializer.errors)

    def test_serializer_with_invalid_golfcourseid(self):
        # Arrange
        invalid_data = {
            'golfcourseid': 'abc',
            'dateplayed': '2023-07-22'
        }

        # Act
        serializer = CreateRoundCommandSerializer(data=invalid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn('golfcourseid', serializer.errors)


if __name__ == '__main__':
    unittest.main()