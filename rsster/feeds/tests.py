import datetime
import unittest
import json

from django.test import TestCase, Client
from .models.feed import Feed
from .models.entry import Entry
from .logic import harvest


class FeedTestCase(TestCase):
    def setUp(self):
        Feed.feeds.create(url='https://example.com/rss.xml', title='the web by example')
        Feed.feeds.create(url='https://notasite.org/rss/index.xml',
                          title='you had been warned', update_interval=71, active=False)
        Feed.feeds.create(url='https://molecule.nl/decorrespondent/rss.php')

    def test_feed_found(self):
        example = Feed.feeds.get(url='https://example.com/rss.xml')
        nosite = Feed.feeds.get(url='https://notasite.org/rss/index.xml')
        self.assertEqual(example.title, 'the web by example')
        self.assertEqual(nosite.title, 'you had been warned')

    def test_harvest(self):
        molecule = Feed.feeds.get(url='https://molecule.nl/decorrespondent/rss.php')
        harvest(molecule)
        latest_entries = Entry.entries.filter(feed__url='https://molecule.nl/decorrespondent/rss.php')\
                                      .order_by('-published').select_related('feed')
        entries = len(latest_entries)
        self.assertEqual(entries, 50)


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


class TestViews(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def testHome(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def testFeed(self):
        response = self.client.get('/feed/1')
        self.assertEqual(response.status_code, 200)

    def testApiPost(self):
        response = self.client.post('/feeds/api/feed',
                                    {"url": "https://www.nrc.nl/rss/"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def testApiPut(self):
        response = self.client.put('/feeds/api/feed',
                                   json.dumps({"url": "https://www.nrc.nl/rss/",
                                               "title": "weer wat nieuws",
                                               "update_interval": "66"}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        content = json.loads(response.content)
        self.assertEqual(len(content), 15)


class FeedparserEntryMock:
    def __init__(self, link=None, title=None, contents=None, summary=None, published_parsed=None):
        self.link = link
        self.title = title
        self.contents = contents
        self.summary = summary
        self.published_parsed = published_parsed
