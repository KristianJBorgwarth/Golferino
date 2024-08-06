from django.db import models
from core.data_access.models.golfcourse_model import Golfcourse
from core.data_access.models.player_model import Player


class Playerround(models.Model):
    playerroundid = models.AutoField(primary_key=True)
    roundid = models.ForeignKey('Round', models.DO_NOTHING, db_column='roundid', blank=True, null=True)
    golfcourseid = models.ForeignKey(Golfcourse, models.OneToOneField, db_column='golfcourseid', blank=True, null=True)
    playerid = models.ForeignKey(Player, models.OneToOneField, db_column='playerid', blank=True, null=True)
    totalscore = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playerround'
