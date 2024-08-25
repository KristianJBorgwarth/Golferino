# command_handlers/create_user_command_handler.py
import logging
from django.contrib.auth.models import User
from core.common.results import Result
from core.data_access.models.verification_code_model import VerificationCode
from core.features.player.commands.create.create_player_command import CreatePlayerCommand
from core.features.player.commands.create.create_player_dto import CreatePlayerDto
from core.common.mediator import RequestHandler
from core.services.email.email_service import EmailService


class CreatePlayerCommandHandler(RequestHandler[CreatePlayerCommand, Result[CreatePlayerDto]]):
    def __init__(self):
        self.email_service = EmailService()
        self.logger = logging.getLogger(__name__)

    def handle(self, command: CreatePlayerCommand) -> Result[CreatePlayerDto]:
        try:
            if User.objects.filter(email=command.email).exists():
                return Result.fail("User with this email already exists.", status_code=400)

            user = User.objects.create_user(
                username=command.email,
                email=command.email,
                password=command.password,
                first_name=command.first_name,
                last_name=command.last_name
            )
            # Generate verification code
            verification_code = VerificationCode(user=user)
            verification_code.save()

            # Send verification email
            self.email_service.send_verification_email(user, verification_code.code)

            # Create user DTO
            user_dto = CreatePlayerDto(user)
            return Result.ok(user_dto.data, status_code=201)

        except Exception as e:
            self.logger.error("An error occurred while handling the command: %s", str(e), exc_info=True)
            return Result.fail("An unexpected error occurred.", status_code=500)
