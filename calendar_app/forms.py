from django import forms
from .models import Location, Event

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ['name', 'parent', 'owner', 'members']


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date']