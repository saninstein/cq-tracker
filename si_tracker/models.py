from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Item(models.Model):

    class Meta:
        abstract = True

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

    type = "Item"
    title = models.CharField(max_length=150, verbose_name="Title")
    date_raised = models.DateField(auto_now_add=True, verbose_name="Date raised")
    date_due = models.DateField(blank=True, verbose_name="Date due")
    description = models.TextField(verbose_name="Description", max_length=5000)
    status = models.CharField(max_length=10, choices=statuses, default=statuses[0], verbose_name="Status")
    visible = models.IntegerField(default=visibility[1], choices=visibility, verbose_name="Visible")
    actions_taken = models.TextField(max_length=5000, verbose_name="Actions taken")

    def __str__(self):
        return self.title

    def get_status(self):
        return [x[1] for x in self.statuses if x[0] == self.status][0]

    def get_visible(self):
        return [x[1] for x in self.visibility if x[0] == self.visible][0]


class Task(Item):
    types = (('T', 'Task'), ('I', 'Idea'))
    raised_by = models.ForeignKey(User, verbose_name="Raised by", related_name='Task')
    assigned_to = models.ForeignKey(User, verbose_name="Assigned to")
    type = models.CharField(max_length=10, choices=types, default=types[0], verbose_name="Type")

    def get_absolute_url(self):
        return reverse('tracker:task', args=[self.id])


class Issue(Item):
    type = "Issue"
    raised_by = models.ForeignKey(User, verbose_name="Raised by", related_name='Issue')
    assigned_to = models.ForeignKey(User, verbose_name="Assigned to")
    related_tasks = models.ManyToManyField(Task, related_name='issue', verbose_name="Related tasks")

    def get_absolute_url(self):
        return reverse('tracker:issue', args=[self.id])