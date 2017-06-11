from django.conf.urls import url
from si_tracker import views

urlpatterns = [
    url(r'^issue/(?P<item>\d+)', views.issue, name='issue'),
    url(r'^task/(?P<item>\d+)', views.task, name='task'),
    url(r'^$', views.items, name='items'),
    url(r'^$', views.general, name='general'),
]