from django.conf.urls import url
from .views import *

urlpatterns = [
    # Locations

    url(r'^locations/$', LocationListView.as_view(), name='locations'),
    url(r'^locations/(?P<pk>\d+)$', LocationDetailView.as_view(), name='location_detail'),
    url(r'^locations/create/$', LocationCreateView.as_view(), name='location_create'),
    url(r'^locations/update/(?P<pk>\d+)$', LocationUpdateView.as_view(), name='location_update'),
    url(r'^locations/delete/(?P<pk>\d+)$', LocationDeleteView.as_view(), name='location_delete'),

    # Events:

    url(r'^api/events/$', EventsApiView.as_view(), name='api_events'),
    url(r'^events/$', EventListView.as_view(), name='events'),
    url(r'^events/create/$', EventCreateView.as_view(), name='event_create'),
    url(r'^events/update/(?P<pk>\d+)$', EventUpdateView.as_view(), name='event_update'),
    url(r'^events/delete/(?P<pk>\d+)$', EventDeleteView.as_view(), name='event_delete'),
]