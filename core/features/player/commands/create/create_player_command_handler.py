import logging
from core.data_access.models.player.player_created_event import PlayerCreatedEvent
from core.data_access.models.verification_code_model import VerificationCode
from core.data_access.repositories.verification_code_repository import VerificationCodeRepository
from core.features.player.commands.create.create_player_command import CreatePlayerCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.player.player_model import Player
from core.common.mediator import RequestHandler
from core.data_access.repositories.player_repository import PlayerRepository
from core.dtos.player_dto import PlayerDto
from core.features.player.commands.create.create_player_dto import CreatePlayerDto
from core.services.password.password_service import PasswordService
from core.services.verification_code.verification_code_service import VerificationCodeService


class CreatePlayerCommandHandler(RequestHandler[CreatePlayerCommand, Result[PlayerDto]]):
    def __init__(self):
        self.player_repository = PlayerRepository(Player)
        self.password_service = PasswordService()
        self.verification_code_service = VerificationCodeService()
        self.verification_code_repository = VerificationCodeRepository(VerificationCode)
        self.logger = logging.getLogger(__name__)
    
    def handle(self, command: CreatePlayerCommand) -> Result[PlayerDto]:
        try:
            if self.player_repository.exists(email=command.email):
                return Result.fail(ErrorMessage.already_exists(str(player.email)), status_code=400)
            
            hashed_password = self.password_service.hash_password(command.password)
            
            player = Player(firstname = command.firstname, 
                            lastname = command.lastname, 
                            email = command.email, 
                            password = hashed_password, 
                            is_verified = False)
            verificationCode = self.verification_code_service.generate_verification_code(player)
            
            player.add_event(PlayerCreatedEvent(player= player, code= verificationCode))
            
            player = self.player_repository.create(player)
            verificationCode = self.verification_code_repository.create(verificationCode)
            
            playerDto = CreatePlayerDto(player)
            return Result.ok(playerDto.data, status_code=200)
        
        except Exception as e:
            self.logger.error("An error occurred while handling the command: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)