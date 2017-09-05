from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^locations/$', LocationListView.as_view(), name='locations'),
    url(r'^location/(?P<pk>\d+)$', LocationDetailView.as_view(), name='location_detail'),
    url(r'^location/create/$', LocationCreateView.as_view(), name='location_create'),
    url(r'^location/update/(?P<pk>\d+)$', LocationUpdateView.as_view(), name='location_update'),
    url(r'^location/delete/(?P<pk>\d+)$', LocationDeleteView.as_view(), name='location_delete'),
]