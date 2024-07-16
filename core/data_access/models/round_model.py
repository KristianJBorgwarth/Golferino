from django.db import models
from core.data_access.models.golfcourse_model import Golfcourse


class Round(models.Model):
    roundid = models.IntegerField(primary_key=True)
    golfcourseid = models.ForeignKey(Golfcourse, models.DO_NOTHING, db_column='golfcourseid', blank=True, null=True)
    dateplayed = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'round'
