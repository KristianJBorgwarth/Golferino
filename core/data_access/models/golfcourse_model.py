from django.db import models


class Golfcourse(models.Model):
    golfcourseid = models.IntegerField(primary_key=True)
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    numholes = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'golfcourse'
