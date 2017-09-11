from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^messages/$', MessageListView.as_view(), name='messages'),
    url(r'^messages/(?P<pk>\d+)$', MessageDetailView.as_view(), name='message'),
]
