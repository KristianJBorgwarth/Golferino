from django.urls import path

from core.views.location_view import LocationView
from core.views.player_view import PlayerView

urlpatterns = [
    path('players/', PlayerView.as_view({'post': 'create'}), name='player-post'),  # Assuming this is for POST requests
    path('players/get_by_id/', PlayerView.as_view({'get': 'get_by_id'}), name='player-by-id'),
    path('players/get_by_name/', PlayerView.as_view({'get': 'get_by_name'}), name='player-by-name'),
    path('locations/', LocationView.as_view({'post': 'create'}), name='location-create'),

]
