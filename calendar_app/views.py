from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import LocationForm, EventForm
from .models import Location, Event

# Locations:

class LocationViewMixin(LoginRequiredMixin):
    model = Location
    context_object_name = "location"
    form_class = LocationForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super(LocationViewMixin, self).dispatch(request, *args, **kwargs)


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
    template_name = "location_form_update/index.html"


# Events:
class EventPassesTestMixin(UserPassesTestMixin):

    raise_exception = PermissionDenied

    def test_func(self):
        user = self.request.user
        return user.Location.filter(owner=user) or user.is_staff


class EventViewMixin(EventPassesTestMixin, LoginRequiredMixin):
    model = Event
    form_class = EventForm
    context_object_name = 'event'
    success_url = reverse_lazy("calendar:events")


class EventFormMixin(ModelFormMixin):

    request = None

    def get_form_kwargs(self):
        kwargs = super(EventFormMixin, self).get_form_kwargs()
        user = self.request.user

        if user.is_staff:
            return kwargs

        locations = Location.objects.filter(owner=user)
        if locations.count():
            kwargs['locations'] = locations
            return kwargs

        raise PermissionDenied()


class EventListView(EventViewMixin, ListView):
    context_object_name = "events"
    template_name = "events/index.html"

    def get_queryset(self):
        location = get_object_or_404(Location, owner=self.request.user)
        return Event.objects.filter(location=location)


class EventCreateView(EventViewMixin, EventFormMixin, CreateView):
    template_name = "event_form_create/index.html"


class EventUpdateView(EventViewMixin, EventFormMixin, UpdateView):
    template_name = "event_form_update/index.html"


class EventDeleteView(EventViewMixin, DeleteView):
    template_name = "event_delete_confirm/index.html"


class EventsApiView(LoginRequiredMixin, View):

    def get(self, req):
        location = Location.objects.filter(Q(members__id=req.user.id) | Q(owner__id=req.user.id))
        if not location:
            raise Http404
        location = location[0]
        return JsonResponse({
            'events': list(Event.objects.filter(location=location).values('id', 'date', 'name')),
            'can_add_events': location.owner == req.user
        })





