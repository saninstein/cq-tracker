from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Item(models.Model):

    class Meta:
        abstract = True
        ordering = ['-date_raised', '-id']

    statuses = (
        ('Open-New', 'Open-New'),
        ('In Progress', 'In Progress'),
        ('Closed-Resolved', 'Closed-Resolved'),
        ('Closed-NotResolved', 'Closed-NotResolved')
    )

    visibility = (
        ('Private', 'Private'),
        ('Public', 'Public')
    )

    type = "Item"
    title = models.CharField(max_length=150, verbose_name="Title")
    date_raised = models.DateField(auto_now_add=True, verbose_name="Date raised")
    date_due = models.DateField(blank=True, verbose_name="Date due")
    description = models.TextField(verbose_name="Description", max_length=5000)
    status = models.CharField(max_length=20, choices=statuses, default=statuses[0], verbose_name="Status")
    visible = models.CharField(max_length=10, default=visibility[1], choices=visibility, verbose_name="Visible")
    actions_taken = models.TextField(max_length=5000, verbose_name="Actions taken")

    def __str__(self):
        return self.title


class Issue(Item):
    type = "Issue"
    raised_by = models.ForeignKey(User, verbose_name="Raised by", related_name='Issue')
    assigned_to = models.ForeignKey(User, verbose_name="Assigned to")
    # related_tasks = models.ManyToManyField(Task, related_name='issue', verbose_name="Related tasks")

    def get_absolute_url(self):
        return reverse('tracker:item', args=['issue', self.id])


class Task(Item):
    types = (('Task', 'Task'), ('Idea', 'Idea'))
    raised_by = models.ForeignKey(User, verbose_name="Raised by", related_name='Task')
    assigned_to = models.ForeignKey(User, verbose_name="Assigned to")
    type = models.CharField(max_length=10, choices=types, default=types[0], verbose_name="Type")
    issue = models.ForeignKey(Issue, verbose_name='Issue')

    def get_absolute_url(self):
        return reverse('tracker:item', args=['task', self.id])