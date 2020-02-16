from django.db import models
from . import Feed
import datetime
import time


class Entry(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField(blank=True, default='')
    contents = models.TextField(blank=True, default='')
    url = models.CharField(db_index=True, max_length=255)
    guid = models.CharField(blank=True, max_length=255)
    last_update = models.DateTimeField(auto_now=True)
    entry_created = models.DateTimeField(auto_now_add=True)
    published = models.CharField(max_length=20, db_index=True, blank=True, default='')

    entries = models.Manager()

    def __str__(self):
        return "%s %s %s [%s]" % (self.id, self.published, self.title, self.feed)

    class Meta:
        verbose_name_plural = "entries"

    def parse_and_create(self, entry, feed):
        """ digest python_feedparser entries and creates rsspy entries """
        if not hasattr(entry, 'link'):
            return False

        contents = ''
        if hasattr(entry, 'content'):
            contents = entry.content[0].value
        if hasattr(entry, 'summary_detail') and len(entry.summary_detail.get('value')) > len(contents):
            contents = entry.summary_detail.get('value', None)
        elif len(entry.summary) > len(contents):
            contents = entry.summary
        if hasattr(entry, 'published_parsed'):
            published = datetime.datetime(*(entry.published_parsed[0:6])).strftime('%Y-%m-%d %H:%M:%S')
        else:
            published = time.strftime('%Y-%m-%d %H:%M:%S')
        # add an image
        if hasattr(entry, 'links'):
            for r in entry.links:
                if (r.get('rel', None) == 'enclosure'
                        and 'image' in r.get('type', None)
                        and r.get('href') not in contents):
                    contents = contents + ' <br/><img src="%s">' % r.get('href', "#")

        item, created = Entry.entries.get_or_create(feed=feed, title=entry.title, url=entry.link)
        if created:
            item.description = entry.summary
            item.contents = contents
            item.guid = entry.link
            item.published = published
            item.save()
