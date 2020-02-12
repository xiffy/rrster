from .models import Feed, Entry
import datetime
import time
import feedparser


def harvest(feed=None):
    if not feed:
        return False
    ts = time.time()
    if feed and isinstance(feed, Feed):
        response = feedparser.parse(feed.url, agent="rsspy harvester 0.9 (https://github.com/xiffy/rsspy)")
        if response.get('status', None):
            if response.status in [200, 301, 302, 307]:
                _parse_feed(feed, response.feed)
                for entry in response.entries:
                    added = Entry().parse_and_create(entry, feed)
                    if added:
                        feed.feed_last_update = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                if response.status in [301, 302, 307]:
                    feed.url = response.get('href', feed.url)
            elif response.status in [410, 404]:
                feed.active = 0
        else:
            print("Timeout")
        feed.last_update = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        feed.save()


def _parse_feed(feed, response_feed):
    feed.title = response_feed.title if hasattr(response_feed, 'title') else ''
    feed.description = response_feed.sub_title if hasattr(response_feed, 'sub_title') else ''
    feed.image = response_feed.image.get('ref', '') if hasattr(response_feed, 'image') else ''
    for link in response_feed.links:
        if link.get('type', None) == 'text/html' and link.get('rel', None) == 'alternate':
            feed.web_url = link.href
    return True
