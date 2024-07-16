from django.urls import path
from core.views.player_view import PlayerView

urlpatterns = [
    path('players/', PlayerView.as_view({'post': 'post'}), name='player-post'),  # Assuming this is for POST requests
    path('player/get_by_id/', PlayerView.as_view({'get': 'get_by_id'}), name='player-by-id'),
    path('player/get_by_name/', PlayerView.as_view({'get': 'get_by_name'}), name='player-by-name'),
]
