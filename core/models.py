# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Golfcourse(models.Model):
    golfcourseid = models.IntegerField(primary_key=True)
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    numholes = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'golfcourse'


class Golfhole(models.Model):
    golfholeid = models.IntegerField(primary_key=True)
    golfcourseid = models.ForeignKey(Golfcourse, models.DO_NOTHING, db_column='golfcourseid', blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    par = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'golfhole'


class Location(models.Model):
    locationid = models.IntegerField(primary_key=True)
    locationname = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class Player(models.Model):
    playerid = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player'


class Playerround(models.Model):
    playerroundid = models.IntegerField(primary_key=True)
    roundid = models.ForeignKey('Round', models.DO_NOTHING, db_column='roundid', blank=True, null=True)
    golfcourseid = models.ForeignKey(Golfcourse, models.DO_NOTHING, db_column='golfcourseid', blank=True, null=True)
    playerid = models.ForeignKey(Player, models.DO_NOTHING, db_column='playerid', blank=True, null=True)
    totalscore = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playerround'


class Round(models.Model):
    roundid = models.IntegerField(primary_key=True)
    golfcourseid = models.ForeignKey(Golfcourse, models.DO_NOTHING, db_column='golfcourseid', blank=True, null=True)
    dateplayed = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'round'


class Score(models.Model):
    scoreid = models.IntegerField(primary_key=True)
    playerroundid = models.ForeignKey(Playerround, models.DO_NOTHING, db_column='playerroundid', blank=True, null=True)
    golfholeid = models.ForeignKey(Golfhole, models.DO_NOTHING, db_column='golfholeid', blank=True, null=True)
    strokes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'score'
