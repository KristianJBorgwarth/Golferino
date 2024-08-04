from django.urls import path

from core.views.golfcourse_view import GolfcourseView
from core.views.location_view import LocationView
from core.views.player_view import PlayerView
from core.views.playerround_view import PlayerroundView
from core.views.round_view import RoundView

urlpatterns = [
    path('players/', PlayerView.as_view({'post': 'create'}), name='player-post'),  # Assuming this is for POST requests
    path('players/get_all', PlayerView.as_view({'get': 'get_all'}), name='players-get-all'),
    path('players/get_by_id/', PlayerView.as_view({'get': 'get_by_id'}), name='player-by-id'),
    path('players/get_by_name/', PlayerView.as_view({'get': 'get_by_name'}), name='player-by-name'),
    path('locations/', LocationView.as_view({'post': 'create'}), name='location-create'),
    path('locations/get_all', LocationView.as_view({'get': 'get_all'}), name='location-get-all'),
    path('rounds/', RoundView.as_view({'post': 'create'}), name='round-post'),
    path('playerrounds/', PlayerroundView.as_view({'post': 'create'}), name='playerround-post'),
    path('golfcourse/', GolfcourseView.as_view({'post': 'create'}), name='golfcourse-post'),
]
