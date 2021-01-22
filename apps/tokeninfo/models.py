from django.db import models
from rest_framework.authtoken.models import Token


class TokenInfo(models.Model):
    token = models.OneToOneField(Token, on_delete=models.PROTECT)
    limit_usage = models.IntegerField()


class TokenUsage(models.Model):
    token_info = models.ForeignKey(TokenInfo, on_delete=models.PROTECT)
    date = models.DateField()

