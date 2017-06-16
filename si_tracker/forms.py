from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from si_tracker.models import *



class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        exclude = []

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.fields['date_due'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = []

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['date_due'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']


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


