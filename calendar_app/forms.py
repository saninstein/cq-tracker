from django import forms
from .models import Location, Event
from django.contrib.auth.models import User


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ['name', 'parent', 'owner', 'members']


    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        bootstraped_form(self)
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
        self.owner = kwargs.pop('owner', None)

        super(EventForm, self).__init__(*args, **kwargs)
        bootstraped_form(self)
        if not self.owner.is_staff:
            locations = Location.objects.filter(owner=self.owner)
            self.initial['location'] = locations[0]
            # self.fields['location'].widget.attrs['readonly'] = True
            self.fields['location'].queryset = locations




def bootstraped_form(form):
    for key in form.fields:
        form.fields[key].widget.attrs['class'] = 'form-control'

