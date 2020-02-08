from django.http import HttpResponse
from django.template import loader
from .logic import harvest as harvest_one
from feeds.models import Feed, Entry


def index(request):
    template = loader.get_template('feeds/index.html')
    latest_entries = Entry.entries.order_by('-published')[:10]
    context = {'latest_entires': latest_entries}
    return HttpResponse(template.render(context, request))

def harvest(request):
    nrc = Feed.feeds.filter(id=1)[0]
    harvest_one(nrc)
    return HttpResponse("Harvesting done!")