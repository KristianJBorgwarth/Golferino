from django.urls import path

from core.features.golfcourse.golfcourse_view import GolfcourseView
from core.features.golfhole.golfhole_view import GolfholeView
from core.features.location.location_view import LocationView
from core.features.player.player_view import PlayerView
from core.features.playerround.playerround_view import PlayerroundView
from core.features.round.round_view import RoundView
from core.features.score.score_view import ScoreView

urlpatterns = [
    path('players/create', PlayerView.as_view({'post': 'create'}), name='player-post'),  # Assuming this is for POST requests
    path('players/get_all', PlayerView.as_view({'get': 'get_all'}), name='players-get-all'),
    path('locations/create', LocationView.as_view({'post': 'create'}), name='location-create'),
    path('locations/get_all', LocationView.as_view({'get': 'get_all'}), name='location-get-all'),
    path('rounds/create', RoundView.as_view({'post': 'create'}), name='round-post'),
    path('playerrounds/create', PlayerroundView.as_view({'post': 'create'}), name='playerround-post'),
    path('playerrounds/get_all', PlayerroundView.as_view({'get': 'get_all'}), name='playerround-get-all'),
    path('golfcourses/create', GolfcourseView.as_view({'post': 'create'}), name='golfcourse-post'),
    path('golfcourses/get_all', GolfcourseView.as_view({'get': 'get_all'}), name='golfcourse-get-all'),
    path('golfholes/create', GolfholeView.as_view({'post': 'create'}), name='golfhole-post'),
    path('golfholes/get_all', GolfholeView.as_view({'get': 'get_all'}), name='golfhole-get-all'),
    path('scores/create', ScoreView.as_view({'post': 'create'}), name='score-post'),
    path('scores/get_all', ScoreView.as_view({'get': 'get_all'}), name='score-get-all'),
    path('scores/update', ScoreView.as_view({'post': 'update'}), name='score-update'),
]
