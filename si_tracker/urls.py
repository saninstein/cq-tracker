from django.conf.urls import url
from si_tracker import views

urlpatterns = [
    url(r'new/issue/$', views.issue_create_update, name='new_issue'),
    url(r'update/issue/(?P<item>\d+)', views.issue_create_update, name='update_issue'),
    url(r'^issue/(?P<item>\d+)', views.issue, name='issue'),
    url(r'^task/(?P<item>\d+)', views.task, name='task'),
    url(r'^$', views.items, name='items'),
    url(r'^$', views.general, name='general'),
]