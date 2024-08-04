from core.behavior.validation_behavior import ValidationBehavior
from core.commands.location.create.create_location_command import CreateLocationCommand
from core.commands.location.create.create_location_command_handler import CreateLocationCommandHandler
from core.commands.player.create.create_player_command import CreatePlayerCommand
from core.commands.player.create.create_player_command_handler import CreatePlayerCommandHandler
from core.commands.playerround.create.create_playerround_command import CreatePlayerroundCommand
from core.commands.playerround.create.create_playerround_command_handler import CreatePlayerroundCommandHandler
from core.commands.round.create.create_round_command import CreateRoundCommand
from core.commands.round.create.create_round_command_handler import CreateRoundCommandHandler
from core.common.mediator import Mediator
from core.queries.location.get.get_locations_query import GetLocationsQuery
from core.queries.location.get.get_locations_query_handler import GetLocationsQueryHandler
from core.queries.player.get.get_players_query import GetPlayersQuery
from core.queries.player.get.get_players_query_handler import GetPlayersQueryHandler
from core.serializers.location.create_location_cmd_serializer import CreateLocationCommandSerializer
from core.serializers.location.get_locations_query_serializer import GetLocationsQuerySerializer
from core.serializers.player.create_player_cmd_serializer import CreatePlayerCommandSerializer
from core.serializers.player.get_players_query_serializer import GetPlayersQuerySerializer
from core.serializers.playerround.create_playerround_cmd_serializer import CreatePlayerroundCommandSerializer
from core.serializers.round.create_round_cmd_serializer import CreateRoundCommandSerializer

# Initialize a single instance of the mediator
mediator = Mediator()

def register_handlers():
    """
    Register all request handlers with the mediator.
    This function is called once at application startup.
    """
    # PlayerRound
    mediator.register_pipeline(CreatePlayerroundCommand, [lambda: ValidationBehavior(CreatePlayerroundCommandSerializer), lambda: CreatePlayerroundCommandHandler()])

    # Player
    mediator.register_pipeline(CreatePlayerCommand, [lambda: ValidationBehavior(CreatePlayerCommandSerializer), lambda: CreatePlayerCommandHandler()])
    mediator.register_pipeline(GetPlayersQuery,[lambda: ValidationBehavior(GetPlayersQuerySerializer), lambda: GetPlayersQueryHandler()])

    # Round
    mediator.register_pipeline(CreateRoundCommand, [lambda: ValidationBehavior(CreateRoundCommandSerializer), lambda: CreateRoundCommandHandler()])

    # Location
    mediator.register_pipeline(GetLocationsQuery,[lambda: ValidationBehavior(GetLocationsQuerySerializer), lambda: GetLocationsQueryHandler()])
    mediator.register_pipeline(CreateLocationCommand, [lambda: ValidationBehavior(CreateLocationCommandSerializer), lambda: CreateLocationCommandHandler()])



def get_mediator() -> Mediator:
    """
    Get the mediator instance.
    This function can be used to access the mediator elsewhere in the application.
    """
    return mediator
