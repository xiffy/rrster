# Grou, model for combining different feeds
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Group(models.Model):
    description = models.CharField(db_index=True, max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.description)


