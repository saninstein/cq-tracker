from django.conf.urls import url
from si_tracker import views

urlpatterns = [
    url(r'^$', views.general, name='general'),
]