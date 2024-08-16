from django.db import models


class Player(models.Model):
    playerid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'player'
