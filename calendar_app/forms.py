from django import forms
from django.db.models import Q
from .models import Location, Event
from django.contrib.auth.models import User


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ['name', 'parent', 'owner', 'members']


    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        bootstraped_form(self)

        if 'instance' not in kwargs:
            self.fields['members'].queryset = User.objects.filter(location=None)

        self.fields['owner'].queryset = User.objects.filter(location=None)
        # Styles
        self.fields['members'].widget.attrs['class'] += " selectpicker"
        self.fields['owner'].widget.attrs['class'] += " selectpicker"
        self.fields['owner'].widget.attrs['data-live-search'] = "true"
        self.fields['members'].widget.attrs['data-live-search'] = "true"



class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date', 'location']

    def __init__(self, user=None, *args, **kwargs):

        # !!!
        self.locations = kwargs.pop('locations', None)

        super(EventForm, self).__init__(*args, **kwargs)
        bootstraped_form(self)
        if self.locations:
            self.fields['location'].queryset = self.locations


def bootstraped_form(form):
    for key in form.fields:
        form.fields[key].widget.attrs['class'] = 'form-control'

