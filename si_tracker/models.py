from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    statuses = (
        ('on', 'Open-New'),
        ('ip', 'In Progress'),
        ('cr', 'Closed-Resolved'),
        ('cn', 'Closed-NotResolved')
    )

    visibility = (
        (0, 'Private'),
        (1, 'Public')
    )

    title = models.CharField(max_length=150, verbose_name="Title")
    raised_by = models.ForeignKey(User, verbose_name="Raised by", related_name='items')
    assigned_to = models.ForeignKey(User, verbose_name="Assigned to")
    date_raised = models.DateField(auto_now_add=True, verbose_name="Date raised")
    date_due = models.DateField(blank=True, verbose_name="Date due")
    description = models.TextField(verbose_name="Description", max_length=5000)
    status = models.CharField(max_length=10, choices=statuses, default=statuses[0], verbose_name="Status")
    visible = models.IntegerField(default=visibility[1], choices=visibility, verbose_name="Visible")


class Task(Item):
    types = (('T', 'Task'), ('I', 'Idea'))
    type = models.CharField(max_length=10, choices=types, default=types[0], verbose_name="Type")


class Issue(Item):
    related_tasks = models.ForeignKey(Task, related_name='issue', verbose_name="Related tasks")