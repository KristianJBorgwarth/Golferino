from django.db import models

from core.data_access.models.location_model import Location


class Golfcourse(models.Model):
    golfcourseid = models.BigAutoField(primary_key=True)
    locationid = models.ForeignKey(Location, db_column='locationid', on_delete=models.CASCADE)
    numholes = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'golfcourse'
