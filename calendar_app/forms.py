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

        print(kwargs)
        if kwargs.get('instance', None) is None:
            self.fields['owner'].queryset = User.objects.filter(Location=None, Location_member=None)
            self.fields['members'].queryset = User.objects.filter(Location=None, Location_member=None)
        # Styles
        self.fields['members'].widget.attrs['class'] += " selectpicker"
        self.fields['owner'].widget.attrs['class'] += " selectpicker"
        self.fields['owner'].widget.attrs['data-live-search'] = "true"
        self.fields['members'].widget.attrs['data-live-search'] = "true"

    def clean(self):
        super(LocationForm, self).clean()
        cleaned_data = self.cleaned_data
        print(cleaned_data.get('owner', None), cleaned_data.get('members', (None, )))
        if cleaned_data['owner'] in cleaned_data['members']:
            self.add_error('owner', "User owner in members!")



class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date', 'location']

    def __init__(self, user=None, *args, **kwargs):

        # !!!
        self.locations = kwargs.pop('locations', None)

        super(EventForm, self).__init__(*args, **kwargs)
        bootstraped_form(self)
        self.fields['date'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']
        if self.locations:
            self.fields['location'].queryset = self.locations


def bootstraped_form(form):
    for key in form.fields:
        form.fields[key].widget.attrs['class'] = 'form-control'

