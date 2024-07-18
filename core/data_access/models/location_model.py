from django.db import models


class Location(models.Model):
    locationid = models.AutoField(primary_key=True)
    locationname = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'
