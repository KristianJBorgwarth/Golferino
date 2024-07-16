from django.urls import path
from core.views.player_view import PlayerView

urlpatterns = [
    path('players/', PlayerView.as_view({'post': 'player-post'})),  # Assuming this is for POST requests
    path('players/get_by_id', PlayerView.as_view({'get': 'get_by_id'})),
    path('players/get_by_name', PlayerView.as_view({'get': 'get_by_name'}))
]
