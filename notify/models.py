from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):

    class Meta:
        ordering = ['-id']

    ISSUE = 'Critical Questions'
    TASK = 'Task'

    description = models.TextField(max_length=1000)
    when = models.DateTimeField(auto_now_add=True)
    type_item = models.CharField(max_length=20, choices=[(ISSUE, ISSUE), (TASK, TASK)])
    item_issue = models.ForeignKey('si_tracker.Issue', blank=True, null=True)
    item_task = models.ForeignKey('si_tracker.Task', blank=True, null=True)

    read = models.BooleanField(default=False)

    user = models.ForeignKey(User)

