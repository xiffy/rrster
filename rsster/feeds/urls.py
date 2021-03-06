"""rsster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('harvest', views.harvest, name='harvest'),
    path('feed/<int:feedid>', views.feed_view, name='feed'),
    path('feeds/api/feed', views.api_feed, name='api_feeds'),
    path('feeds/api/feed/<int:feedid>', views.api_feed, name='api_feeds_feed'),
    path('group/<int:groupid>', views.group_view, name='groupview'),
]
