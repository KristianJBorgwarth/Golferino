import os
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.data_access.models.location_model import Location
from core.data_access.models.golfcourse_model import Golfcourse
from core.data_access.models.golfhole_model import Golfhole
from core.data_access.models.player.player_model import Player
from core.data_access.models.round_model import Round
from core.data_access.models.playerround_model import Playerround
from core.data_access.models.score_model import Score

from datetime import date

# Insert Location
location = Location(locationname='Tange Sø Golfklub', address='Tange Søvej 68', city='8840 Rødkærsbro')
location.save()

# Insert GolfCourse
golfcourse = Golfcourse(locationid=location, numholes=9, name='TIKMA COURSE PAY&PLAY')
golfcourse.save()

# Insert GolfHoles
holes = [
    Golfhole(golfcourseid=golfcourse, length=112, par=3, number=1),
    Golfhole(golfcourseid=golfcourse, length=70, par=3, number=2),
    Golfhole(golfcourseid=golfcourse, length=100, par=3, number=3),
    Golfhole(golfcourseid=golfcourse, length=77, par=3, number=4),
    Golfhole(golfcourseid=golfcourse, length=75, par=3, number=5),
    Golfhole(golfcourseid=golfcourse, length=62, par=3, number=6),
    Golfhole(golfcourseid=golfcourse, length=85, par=3, number=7),
    Golfhole(golfcourseid=golfcourse, length=60, par=3, number=8),
    Golfhole(golfcourseid=golfcourse, length=100, par=3, number=9),
]
Golfhole.objects.bulk_create(holes)

# Insert Players
player1 = Player(firstname='Lasse', lastname='Rando', email='lasse.Rando@example.com')
player2 = Player(firstname='Jeppe', lastname='Rando', email='jeppe.Rando@example.com')
player1.save()
player2.save()

# Insert Round
round_instance = Round(golfcourseid=golfcourse, dateplayed=date(2024, 5, 10))
round_instance.save()

# Insert PlayerRounds
playerround1 = Playerround(roundid=round_instance, playerid=player1, totalscore=43)
playerround2 = Playerround(roundid=round_instance, playerid=player2, totalscore=44)
playerround1.save()
playerround2.save()

# Insert Scores for Lasse
scores_lasse = [
    Score(playerroundid=playerround1, golfholeid=holes[0], strokes=6),
    Score(playerroundid=playerround1, golfholeid=holes[1], strokes=5),
    Score(playerroundid=playerround1, golfholeid=holes[2], strokes=5),
    Score(playerroundid=playerround1, golfholeid=holes[3], strokes=5),
    Score(playerroundid=playerround1, golfholeid=holes[4], strokes=5),
    Score(playerroundid=playerround1, golfholeid=holes[5], strokes=3),
    Score(playerroundid=playerround1, golfholeid=holes[6], strokes=4),
    Score(playerroundid=playerround1, golfholeid=holes[7], strokes=5),
    Score(playerroundid=playerround1, golfholeid=holes[8], strokes=5),
]
Score.objects.bulk_create(scores_lasse)

# Insert Scores for Jeppe
scores_jeppe = [
    Score(playerroundid=playerround2, golfholeid=holes[0], strokes=5),
    Score(playerroundid=playerround2, golfholeid=holes[1], strokes=5),
    Score(playerroundid=playerround2, golfholeid=holes[2], strokes=7),
    Score(playerroundid=playerround2, golfholeid=holes[3], strokes=5),
    Score(playerroundid=playerround2, golfholeid=holes[4], strokes=6),
    Score(playerroundid=playerround2, golfholeid=holes[5], strokes=3),
    Score(playerroundid=playerround2, golfholeid=holes[6], strokes=3),
    Score(playerroundid=playerround2, golfholeid=holes[7], strokes=5),
    Score(playerroundid=playerround2, golfholeid=holes[8], strokes=5),
]
Score.objects.bulk_create(scores_jeppe)
