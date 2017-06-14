from django.conf.urls import url
from si_tracker import views

urlpatterns = [
    url(r'^new/(?P<type>[\w\-]+)/$', views.item_create_update, name='new_item'),
    url(r'^update/(?P<type>[\w\-]+)/(?P<item>\d+)', views.item_create_update, name='update_item'),
    url(r'^item/(?P<type>[\w\-]+)/(?P<item>\d+)', views.item, name='item'),
    url(r'^items/', views.items, name='items'),
    url(r'^$', views.general, name='general'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^delete/(?P<type>[\w\-]+)/(?P<item>\d+)', views.delete_item, name='delete_item'),
]