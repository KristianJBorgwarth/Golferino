from django.contrib.auth.models import User
from django.db import models


class VerificationCode(models.Model):
    code_id = models.AutoField(primary_key=True)
    player = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_code', db_column='id')
    code = models.CharField(max_length=8)
    is_used = models.BooleanField()
    expiration_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'verification_code'
