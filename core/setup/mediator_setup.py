from core.behavior.validation_behavior import ValidationBehavior
from core.data_access.models.player.player_created_event import PlayerCreatedEvent
from core.features.golfcourse.commands.create.create_golfcourse_command import CreateGolfcourseCommand
from core.features.golfcourse.commands.create.create_golfcourse_command_handler import CreateGolfcourseCommandHandler
from core.features.golfhole.commands.create.create_golfhole_command import CreateGolfholeCommand
from core.features.golfhole.commands.create.create_golfhole_command_handler import CreateGolfholeCommandHandler
from core.features.location.commands.create.create_location_command import CreateLocationCommand
from core.features.location.commands.create.create_location_command_handler import CreateLocationCommandHandler
from core.features.player.commands.create.create_player_command import CreatePlayerCommand
from core.features.player.commands.create.create_player_command_handler import CreatePlayerCommandHandler
from core.features.player.events.player_created_event_handler import PlayerCreatedEventHandler
from core.features.playerround.commands.create.create_playerround_command import CreatePlayerroundCommand
from core.features.playerround.commands.create.create_playerround_command_handler import CreatePlayerroundCommandHandler
from core.features.round.commands.create.create_round_command import CreateRoundCommand
from core.features.round.commands.create.create_round_command_handler import CreateRoundCommandHandler
from core.features.score.commands.create.create_score_command import CreateScoreCommand
from core.features.score.commands.create.create_score_command_handler import CreateScoreCommandHandler
from core.common.mediator import Mediator
from core.features.golfcourse.queries.get.get_golfcourses_query import GetGolfcoursesQuery
from core.features.golfcourse.queries.get.get_golfcourses_query_handler import GetGolfcoursesQueryHandler
from core.features.location.queries.get.get_locations_query import GetLocationsQuery
from core.features.location.queries.get.get_locations_query_handler import GetLocationsQueryHandler
from core.features.player.queries.get.get_players_query import GetPlayersQuery
from core.features.player.queries.get.get_players_query_handler import GetPlayersQueryHandler
from core.features.playerround.queries.get.get_playerrounds_query import GetPlayerroundsQuery
from core.features.playerround.queries.get.get_playerrounds_query_handler import GetPlayerroundsQueryHandler
from core.features.golfcourse.commands.create.create_golfcourse_cmd_serializer import CreateGolfcourseCommandSerializer
from core.features.golfcourse.queries.get.get_golfcourses_query_serializer import GetGolfcoursesQuerySerializer
from core.features.golfhole.commands.create.create_golfhole_cmd_serializer import CreateGolfholeCommandSerializer
from core.features.location.commands.create.create_location_cmd_serializer import CreateLocationCommandSerializer
from core.features.location.queries.get.get_locations_query_serializer import GetLocationsQuerySerializer
from core.features.player.commands.create.create_player_cmd_serializer import CreatePlayerCommandSerializer
from core.features.player.queries.get.get_players_query_serializer import GetPlayersQuerySerializer
from core.features.playerround.commands.create.create_playerround_cmd_serializer import CreatePlayerroundCommandSerializer
from core.features.playerround.queries.get.get_playerrounds_query_serializer import GetPlayerroundsQuerySerializer
from core.features.round.commands.create.create_round_cmd_serializer import CreateRoundCommandSerializer
from core.features.score.commands.create.create_score_cmd_serializer import CreateScoreCommandSerializer

# Initialize a single instance of the mediator
mediator = Mediator()


def register_handlers():
    """
    Register all request handlers with the mediator.
    This function is called once at application startup.
    """
    # PlayerRound
    mediator.register_pipeline(CreatePlayerroundCommand, [lambda: ValidationBehavior(CreatePlayerroundCommandSerializer), lambda: CreatePlayerroundCommandHandler()])
    mediator.register_pipeline(GetPlayerroundsQuery,[lambda: ValidationBehavior(GetPlayerroundsQuerySerializer), lambda: GetPlayerroundsQueryHandler()])

    # Player
    mediator.register_pipeline(CreatePlayerCommand, [lambda: ValidationBehavior(CreatePlayerCommandSerializer), lambda: CreatePlayerCommandHandler()])
    mediator.register_pipeline(GetPlayersQuery,[lambda: ValidationBehavior(GetPlayersQuerySerializer), lambda: GetPlayersQueryHandler()])

    # Round
    mediator.register_pipeline(CreateRoundCommand, [lambda: ValidationBehavior(CreateRoundCommandSerializer), lambda: CreateRoundCommandHandler()])

    # Location
    mediator.register_pipeline(GetLocationsQuery,[lambda: ValidationBehavior(GetLocationsQuerySerializer), lambda: GetLocationsQueryHandler()])
    mediator.register_pipeline(CreateLocationCommand, [lambda: ValidationBehavior(CreateLocationCommandSerializer), lambda: CreateLocationCommandHandler()])

    # Golfcourse
    mediator.register_pipeline(CreateGolfcourseCommand, [lambda: ValidationBehavior(CreateGolfcourseCommandSerializer), lambda: CreateGolfcourseCommandHandler()])
    mediator.register_pipeline(GetGolfcoursesQuery, [lambda: ValidationBehavior(GetGolfcoursesQuerySerializer), lambda: GetGolfcoursesQueryHandler()])

    # Golfhole
    mediator.register_pipeline(CreateGolfholeCommand, [lambda: ValidationBehavior(CreateGolfholeCommandSerializer), lambda: CreateGolfholeCommandHandler()])

    # Score
    mediator.register_pipeline(CreateScoreCommand, [lambda: ValidationBehavior(CreateScoreCommandSerializer), lambda: CreateScoreCommandHandler()])
    
    
    #EVENTS ------------------------------------------------------

def get_mediator() -> Mediator:
    """
    Get the mediator instance.
    This function can be used to access the mediator elsewhere in the application.
    """
    return mediator
