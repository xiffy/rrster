from django.http import HttpResponse, Http404
from django.template import loader
from .logic import harvest as harvest_one
from feeds.models import Feed, Entry


def index(request):
    template = loader.get_template('feeds/index.html')
    latest_entries = Entry.entries.filter(feed__active=True).order_by('-published').select_related('feed')
    context = {'latest_entries': latest_entries}
    return HttpResponse(template.render(context, request))

def feed_view(request, id=None):
    if not id:
        raise Http404("Please provide a FeedId")
    else:
        template = loader.get_template('feeds/index.html')
        feed_entries = Entry.entries.filter(feed__id=id, feed__active=True)
        context = {'latest_entries': feed_entries}
        return HttpResponse(template.render(context, request))


def harvest(request):
    candidates = Feed.feeds.filter(active=True)
    for site in candidates:
        harvest_one(site)
    return HttpResponse("Harvesting done!")