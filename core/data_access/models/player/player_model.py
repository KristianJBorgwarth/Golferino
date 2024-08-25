from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Player(AbstractBaseUser):
    playerid = models.AutoField(primary_key=True)
    is_verified = models.BooleanField(blank=True, null=True)
    USERNAME_FIELD = "playerid"
    class Meta:
        managed = True
        db_table = 'player'
