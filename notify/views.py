from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Message, MessageProfile


class MessageViewMixin(LoginRequiredMixin):
    model = Message
    context_object_name = "message"


class MessageListView(MessageViewMixin, ListView):
    context_object_name = "messages"
    template_name = "messages/index.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class MessageUserPassetTestMixin(UserPassesTestMixin):
    raise_exception = PermissionDenied

    def test_func(self):
        self.object = self.get_object()
        return self.object.user == self.request.user


class MessageDetailView(MessageUserPassetTestMixin, MessageViewMixin, DetailView):
    template_name = "message/index.html"

    def get_context_data(self, **kwargs):
        self.object.read = True
        self.object.save()
        return super(MessageDetailView, self).get_context_data(**kwargs)


class MessageProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = MessageProfile
    context_object_name = 'messageprofile'
    fields = ('allow_email_events',)
    template_name = "messageprofile_form/index.html"
    success_url = reverse_lazy('tracker:users')

    raise_exception = PermissionDenied

    def test_func(self):
        return self.request.user.is_staff



