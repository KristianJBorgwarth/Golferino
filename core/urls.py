from django.urls import path
from core.views.player_view import PlayerView

urlpatterns = [
    path('players/', PlayerView.as_view(), name='player-post'),
 ]
