from django.db import models
from core.data_access.models.golfcourse_model import Golfcourse


class Golfhole(models.Model):
    golfholeid = models.IntegerField(primary_key=True)
    golfcourseid = models.ForeignKey(Golfcourse, models.DO_NOTHING, db_column='golfcourseid', blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    par = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'golfhole'
