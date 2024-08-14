from django.db import models 


class VerificationCode(models.Model):
    code_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=8)
    is_used = models.BooleanField()
    expiration_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'verification_code'