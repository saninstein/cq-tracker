from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Location


class LocationViewMixin:
    model = Location
    context_object_name = "location"
    fields = ['name', 'parent', 'owner', 'members']

class LocationListView(LocationViewMixin, ListView):
    template_name = "locations/index.html"
    context_object_name = "locations"

class LocationDetailView(LocationViewMixin, DetailView):
    template_name = "location/index.html"


class LocationCreateView(LocationViewMixin, CreateView):
    template_name = "location_form_create/index.html"


class LocationDeleteView(LocationViewMixin, DeleteView):
    template_name = "location_delete_confirm/index.html"
    success_url = reverse_lazy("calendar:locations")


class LocationUpdateView(LocationViewMixin, UpdateView):
    pass



