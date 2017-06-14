from django import forms
from si_tracker.models import *


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        exclude = []

    # def __init__(self, user, *args, **kwargs):
    #     super(IssueForm, self).__init__(*args, **kwargs)
    #     if self.instance:
    #         self.fields['related_tasks'].queryset = Task.objects.filter(raised_by=user)


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = []
