from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now, timedelta


class TokenInfo(models.Model):
    token = models.OneToOneField(Token, on_delete=models.PROTECT)
    limit_usage = models.IntegerField()


class TokeUsage(models.Model):
    token_info = models.ForeignKey(TokenInfo, on_delete=models.PROTECT)
    date = models.DateField()

