from django.db import models
from core.data_access.models.golfhole_model import Golfhole
from core.data_access.models.playerround_model import Playerround


class Score(models.Model):
    scoreid = models.IntegerField(primary_key=True)
    playerroundid = models.ForeignKey(Playerround, models.DO_NOTHING, db_column='playerroundid', blank=True, null=True)
    golfholeid = models.ForeignKey(Golfhole, models.DO_NOTHING, db_column='golfholeid', blank=True, null=True)
    strokes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'score'
