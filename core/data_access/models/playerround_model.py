from django.contrib.auth.models import User
from django.db import models


class Playerround(models.Model):
    playerroundid = models.AutoField(primary_key=True)
    roundid = models.ForeignKey('Round', models.OneToOneField, db_column='roundid', blank=True, null=True)
    playerid = models.ForeignKey(User, models.OneToOneField, db_column='id', blank=True, null=True)
    totalscore = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'playerround'
