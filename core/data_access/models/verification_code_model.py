from django.db import models

from core.data_access.models.player.player_model import Player

class VerificationCode(models.Model):
    code_id = models.AutoField(primary_key=True)
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='verification_code', db_column='playerid')
    code = models.CharField(max_length=8)
    is_used = models.BooleanField()
    expiration_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'verification_code'
