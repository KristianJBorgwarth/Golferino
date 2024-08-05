from core.behavior.validation_behavior import ValidationBehavior
from core.commands.location.create.create_location_command import CreateLocationCommand
from core.commands.location.create.create_location_command_handler import CreateLocationCommandHandler
from core.commands.player.create.create_player_command import CreatePlayerCommand
from core.commands.player.create.create_player_command_handler import CreatePlayerCommandHandler
from core.commands.round.create.create_round_command import CreateRoundCommand
from core.commands.round.create.create_round_command_handler import CreateRoundCommandHandler
from core.commands.playerround.create.create_playerround_command import CreatePlayerroundCommand
from core.commands.playerround.create.create_playerround_command_handler import CreatePlayerroundCommandHandler
from core.common.mediator import Mediator
from core.queries.location.get.get_locations_query import GetLocationsQuery
from core.queries.location.get.get_locations_query_handler import GetLocationsQueryHandler
from core.queries.player.get.get_players_query import GetPlayersQuery
from core.queries.player.get.get_players_query_handler import GetPlayersQueryHandler
from core.serializers.location.create_location_cmd_serializer import CreateLocationCommandSerializer
from core.serializers.location.get_locations_query_serializer import GetLocationsQuerySerializer
from core.serializers.player.get_players_query_serializer import GetPlayersQuerySerializer

# Initialize a single instance of the mediator
mediator = Mediator()


# TODO: Look into handling the registration of handlers dynamically during runtime (instantiating a handler upon request) to avoid potential race conditions, if any?
def register_handlers():
    """
    Register all request handlers with the mediator.
    This function is called once at application startup.
    """
    # Creators
    mediator.register_pipeline(CreateLocationCommand, [lambda: ValidationBehavior(CreateLocationCommandSerializer), lambda: CreateLocationCommandHandler()])
    mediator.register_handler(CreatePlayerCommand, CreatePlayerCommandHandler())
    mediator.register_handler(CreateRoundCommand, CreateRoundCommandHandler())
    mediator.register_handler(CreatePlayerroundCommand, CreatePlayerroundCommandHandler())

    # Getters
    mediator.register_pipeline(GetLocationsQuery,[lambda: ValidationBehavior(GetLocationsQuerySerializer), lambda: GetLocationsQueryHandler()])
    mediator.register_pipeline(GetPlayersQuery,[lambda: ValidationBehavior(GetPlayersQuerySerializer), lambda: GetPlayersQueryHandler()])


def get_mediator() -> Mediator:
    """
    Get the mediator instance.
    This function can be used to access the mediator elsewhere in the application.
    """
    return mediator
