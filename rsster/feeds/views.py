from django.http import HttpResponse
from django.template import loader
from .logic import harvest as harvest_one
from feeds.models import Feed, Entry


def index(request):
    template = loader.get_template('feeds/index.html')
    latest_entries = Entry.entries.order_by('-published')
    context = {'latest_entries': latest_entries}
    return HttpResponse(template.render(context, request))

def harvest(request):
    candidates = Feed.feeds.filter(active=True)
    for site in candidates:
        harvest_one(site)
    return HttpResponse("Harvesting done!")