from django.db import models


class Feed(models.Model):
    url = models.CharField(db_index=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, default='')
    image = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    update_interval = models.IntegerField(default=59)
    feed_last_publication = models.DateTimeField(auto_now_add=True, blank=True)
    web_url = models.CharField(max_length=255, blank=True, default='')
    active = models.BooleanField(default=True)

    feeds = models.Manager()

    def __str__(self):
        return "%s: %s " % (self.url, self.title)