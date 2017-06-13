from django.conf.urls import url
from si_tracker import views

urlpatterns = [
    url(r'^new/(?P<type>[\w\-]+)/$', views.item_create_update, name='new_item'),
    url(r'^update/(?P<type>[\w\-]+)/(?P<item>\d+)', views.item_create_update, name='update_item'),
    url(r'^item/(?P<type>[\w\-]+)/(?P<item>\d+)', views.item, name='item'),
    # url(r'^$', views.items, name='items'),
    url(r'^$', views.general, name='general'),
]