from django.http import HttpResponse, Http404
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .logic import harvest as harvest_one
from .models import Feed, Entry


def index(request):
    template = loader.get_template('feeds/index.html')
    latest_entries = Entry.entries.filter(feed__active=True).order_by('-published').select_related('feed')
    entries = paged(latest_entries, request)
    context = {'latest_entries': entries}
    return HttpResponse(template.render(context, request))


def feed_view(request, id=None):
    if not id:
        raise Http404("Please provide a FeedId")
    template = loader.get_template('feeds/index.html')
    feed_entries = Entry.entries.filter(feed__id=id, feed__active=True).order_by('-published')
    entries = paged(feed_entries, request)
    context = {'latest_entries': entries}
    return HttpResponse(template.render(context, request))


def harvest(request):
    candidates = Feed.feeds.filter(active=True)
    for site in candidates:
        harvest_one(site)
    return HttpResponse("Harvesting done!")


def paged(entries, request):
    page = request.GET.get('page', 1)
    pager = Paginator(entries, 10)
    try:
        entries = pager.page(page)
    except PageNotAnInteger:
        entries = pager.page(1)
    except EmptyPage:
        entries = pager.page(pager.num_pages)
    return entries
