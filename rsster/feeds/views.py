import json
import datetime as dt
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from .logic import harvest as harvest_one
from .models import Feed, Entry, Group


def index(request):
    template = loader.get_template('feeds/index.html')
    latest_entries = Entry.entries.filter(feed__active=True).order_by('-published').select_related('feed')
    entries = paged(latest_entries, request)
    context = {'latest_entries': entries}
    return HttpResponse(template.render(context, request))


def feed_view(request, feedid=None):
    if not feedid:
        raise Http404("Please provide a FeedId")
    template = loader.get_template('feeds/index.html')
    feed_entries = Entry.entries.filter(feed__id=feedid, feed__active=True).order_by('-published')
    entries = paged(feed_entries, request)
    context = {'latest_entries': entries}
    return HttpResponse(template.render(context, request))


def group_view(request, groupid=None):
    if not groupid:
        raise Http404("please provide a valid GroupID")
    group = Group.objects.filter(id=groupid).select_related('user')
    if not group:
        raise Http404("No! please provide a valid GroupID")
    f = Feed.feeds.filter(groups__id=groupid)
    print(f)
    group_entries = Entry.entries.filter(feed__id__in=f, feed__active=True).order_by('-published')[:10]
    print(group_entries)
    return HttpResponse('Hoi')


def harvest(request):
    candidates = Feed.feeds.filter(active=True)
    for site in candidates:
        harvest_one(site)
    return HttpResponse("Harvesting done! - %s" % dt.datetime.now())


@csrf_exempt
def api_feed(request, feedid=None):
    if request.method == 'GET' and feedid:
        feed_entries = Entry.entries.filter(feed__id=feedid, feed__active=True).order_by('-published')[:100]
        return JsonResponse(list(feed_entries.values()), safe=False)
    if request.method == 'POST' and request.POST:
        if request.POST.get('url', None).startswith('http'):
            alreadyhere, created = Feed.feeds.get_or_create(url=request.POST['url'])
            if alreadyhere and created:
                harvest_one(alreadyhere)
            feed_entries = Entry.entries.filter(feed__id=alreadyhere.id, feed__active=True).order_by('-published')[:2]
            return JsonResponse(list(feed_entries.values()), safe=False)
        else:
            return 'Please provide a valid feed-URL'
    if request.method == 'PUT' and request.body:
        data = json.loads(request.body.decode('utf-8'))
        if data.get('url', None):
            try:
                channel = Feed.feeds.get(url=data.get('url'))
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Please provide a known URL'})
            channel.update_interval = data.get('update_interval') \
                if data.get('update_interval', None) else channel.update_interval
            channel.title = data.get('title') if data.get('title', None) else channel.title
            channel.active = data.get('active') if data.get('active', None) else channel.active
            channel.image = data.get('image') if data.get('image', None) else channel.image
            channel.description = data.get('description') if data.get('description', None) else channel.description
            channel.web_url = data.get('web_url') if data.get('web_url', None) else channel.web_url
            channel.save()

            feed_entries = Entry.entries.filter(feed__id=channel.id).order_by('-published')[:15]
            return JsonResponse(list(feed_entries.values()), safe=False)
        return JsonResponse({'error': 'Please provide a known URL'})

    return HttpResponse('%s in je broekje' % request.method)


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
