from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from si_tracker.models import *
from si_tracker.utils import message_create, message_about_task



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

    def save(self, user=None, item=None, commit=True):
        if user and item:
            issue = super(IssueForm, self).save(commit=False)
            try:
                i = Issue.objects.get(id=issue.id)
                if(i.status != issue.status):
                    log = LogIssue()
                    log.what = "Status \"{}\" changed to \"{}\"".format(i.status, issue.status)
                    log.who = user
                    log.item = item
                    log.save()
                    message_create(log.what, item, item.raised_by)
                    message_create(log.what, item, item.assigned_to)
                    message_create(log.what, item, item.location.owner)
            except Issue.DoesNotExist:
                pass
        return super(IssueForm, self).save(commit)


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

    def save(self, user=None, item=None, commit=True):
        if user and item:
            task = super(TaskForm, self).save(commit=False)
            try:
                i = Task.objects.get(id=task.id)
                if(i.status != task.status):
                    log = LogTask()
                    log.what = "Status \"{}\" changed to \"{}\"".format(i.status, task.status)
                    log.who = user
                    log.item = item
                    log.save()
                    message_create(log.what, item, item.raised_by)
                    message_create(log.what, item, item.assigned_to)
                    message_create(log.what, item, item.location.owner)
                    message_about_task("Associated tasks: {}".format(log.what), item)
            except Issue.DoesNotExist:
                pass
        return super(TaskForm, self).save(commit)


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


