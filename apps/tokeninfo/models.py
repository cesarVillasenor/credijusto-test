from django.db import models
from rest_framework.authtoken.models import Token


class TokenInfo(models.Model):
    token = models.OneToOneField(Token, on_delete=models.PROTECT)
    limit_usage = models.IntegerField()

    def __str__(self):
        return self.token.user.username + ' - ' + str(self.token)


class TokenUsage(models.Model):
    token_info = models.ForeignKey(TokenInfo, on_delete=models.PROTECT)
    date = models.DateField()
