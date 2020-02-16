import datetime

from django.test import TestCase
from .models.feed import Feed
from .models.entry import Entry


class FeedTestCase(TestCase):
    def setUp(self):
        Feed.feeds.create(url='https://example.com/rss.xml', title='the web by example')
        Feed.feeds.create(url='https://notasite.org/rss/index.xml',
                          title='you had been warned', update_interval=71, active=False)

    def test_feed_found(self):
        example = Feed.feeds.get(url='https://example.com/rss.xml')
        nosite = Feed.feeds.get(url='https://notasite.org/rss/index.xml')
        self.assertEqual(example.title, 'the web by example')
        self.assertEqual(nosite.title, 'you had been warned')


class EntryTestCase(TestCase):
    def setUp(self):
        example, _ = Feed.feeds.get_or_create(url='https://example.com/rss.xml', title='the web by example')
        nosite, _ = Feed.feeds.get_or_create(url='https://notasite.org/rss/index.xml',
                                             title='you had been warned', update_interval=71, active=False)
        Entry.entries.create(feed=example, title="Story 1", url="https://example.com/story/1",
                             published=datetime.datetime.now())
        Entry.entries.create(feed=example, title="Story 2", url="https://example.com/story/2",
                             published=datetime.datetime.now())
        Entry.entries.create(feed=nosite, title="No Story", url="https://notasite.org/story/0",
                             published=datetime.datetime.now())

    def test_recent_entries(self):
        latest_entries = Entry.entries.filter(feed__active=True).order_by('-published').select_related('feed')
        entries = len(latest_entries)
        self.assertEqual(entries, 2)

    def test_entries_found(self):
        entries = Entry.entries.count()
        self.assertEqual(entries, 3)

    def test_parse_and_create(self):
        example = Feed.feeds.get(url='https://example.com/rss.xml')
        to_parse = FeedparserEntryMock(link='https://example.com/story/3',
                                       contents='lief dagboek, dit is de contents',
                                       summary='lief dagboek ...',
                                       title='This is a story all about how my life got turned',
                                       published_parsed=datetime.datetime.now().timetuple())
        Entry().parse_and_create(entry=to_parse, feed=example)
        entries = Entry.entries.count()
        self.assertEqual(entries, 4)
        latest_entries = Entry.entries.filter(feed__active=True).order_by('-published').select_related('feed')
        entries = len(latest_entries)
        self.assertEqual(entries, 3)


class FeedparserEntryMock:
    def __init__(self, link=None, title=None, contents=None, summary=None, published_parsed=None):
        self.link = link
        self.title = title
        self.contents = contents
        self.summary = summary
        self.published_parsed = published_parsed
