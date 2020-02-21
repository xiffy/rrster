from django.db import models
from . import Group
from . import Feed


class GroupFeed(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return "[%s] %s" % (self.group, self.feed)