from unittest import mock
from unittest.mock import MagicMock
from unittest import TestCase
from core.features.player.commands.create.create_player_command import CreatePlayerCommand
from core.features.player.commands.create.create_player_command_handler import CreatePlayerCommandHandler
from core.data_access.repositories.player_repository import PlayerRepository
from core.services.password.password_service import PasswordService
from core.services.verification_code.verification_code_service import VerificationCodeService
from core.data_access.repositories.verification_code_repository import VerificationCodeRepository
from core.data_access.models.player.player_model import Player
from core.data_access.models.verification_code_model import VerificationCode
from core.common.results import Result


class TestCreatePlayerCommandHandler(TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_player_repository = MagicMock(spec=PlayerRepository)
        self.mock_password_service = MagicMock(spec=PasswordService)
        self.mock_verification_code_service = MagicMock(spec=VerificationCodeService)
        self.mock_verification_code_repository = MagicMock(spec=VerificationCodeRepository)
        self.handler = CreatePlayerCommandHandler()
        self.handler.player_repository = self.mock_player_repository
        self.handler.password_service = self.mock_password_service
        self.handler.verification_code_service = self.mock_verification_code_service
        self.handler.verification_code_repository = self.mock_verification_code_repository

    def test_handle_given_existing_player_should_return_already_exists_error(self):
        # Arrange
        command = CreatePlayerCommand(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com',
            password="validPasswordKJ?=1"
        )
        
        self.mock_player_repository.exists.return_value = True

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, '(Test@mail.com) already exists.')
        self.mock_player_repository.exists.assert_called_once_with(email='Test@mail.com')
        self.mock_player_repository.create.assert_not_called()

    def test_handle_given_valid_command_should_create_and_return_result_ok_playerDto(self):
        # Arrange
        command = CreatePlayerCommand(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com',
            password="validPasswordKJ?=1"
        )
        
        self.mock_player_repository.exists.return_value = False
        self.mock_password_service.hash_password.return_value = 'hashedPassword'

        player = Player(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com',
            password='hashedPassword'
        )

        verification_code = VerificationCode(
            code='123456',
            player=player
        )

        self.mock_verification_code_service.generate_verification_code.return_value = verification_code
        self.mock_player_repository.create.return_value = player
        self.mock_verification_code_repository.create.return_value = verification_code

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertIsInstance(result.value, dict)
        self.assertEqual(result.value['firstname'], 'TestFirstName')
        self.assertEqual(result.value['lastname'], 'TestLastName')
        self.assertEqual(result.value['email'], 'Test@mail.com')
        self.mock_player_repository.exists.assert_called_once_with(email='Test@mail.com')
        self.mock_password_service.hash_password.assert_called_once_with("validPasswordKJ?=1")
        self.mock_verification_code_service.generate_verification_code.assert_called_once_with(mock.ANY)
        self.mock_player_repository.create.assert_called_once_with(mock.ANY)
        self.mock_verification_code_repository.create.assert_called_once_with(verification_code)
