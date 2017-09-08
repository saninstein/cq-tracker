from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from si_tracker.models import *



class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = [
            'title', 'location', 'purpose', 'description', 'output',
            'resources', 'date_due', 'raised_by', 'assigned_to', 'visible',
            'actions_taken', 'status', 'addressed'
        ]

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.fields['date_due'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']
        self.fields['output'].widget.attrs['rows'] = 4
        self.fields['resources'].widget.attrs['rows'] = 4


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            'title', 'type', 'location', 'purpose', 'description', 'output',
            'resources', 'date_due', 'raised_by', 'assigned_to', 'visible',
            'actions_taken', 'status', 'addressed', 'issue'
        ]

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['date_due'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']
        self.fields['output'].widget.attrs['rows'] = 4
        self.fields['resources'].widget.attrs['rows'] = 4
        self.fields['issue'].widget.attrs['data-live-search'] = "true"


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", 'first_name', "password1", "password2", 'is_staff')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Role name"

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UpdateUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "email", 'first_name', 'is_staff')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Role name"

    def clean_password(self):
        return self.initial.get('password', None)


