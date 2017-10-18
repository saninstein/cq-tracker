from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from simple_history.models import HistoricalRecords

class Item(models.Model):

    class Meta:
        abstract = True
        ordering = ['-date_raised', '-id']

    open_statuses = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Overdue', 'Overdue')
    )

    closed_statuses = (
        ('Resolved', 'Resolved'),
        ('NotResolved', 'NotResolved')
    )

    statuses =  open_statuses + closed_statuses

    visibility = (
        ('Private', 'Private'),
        ('Public', 'Public')
    )

    locations = (
        ('Asset Delivery', 'Asset Delivery'), ('Hunter Valley', 'Hunter Valley'),
        ('Central & North West', 'Central & North West'), ('Port Waratah', 'Port Waratah'),
        ('Maitland', 'Maitland'), ('Muswellbrook', 'Muswellbrook'),
        ('Scone', 'Scone'), ('Gunnedah', 'Gunnedah'),
        ('Narrabri', 'Narrabri'), ('Tamworth', 'Tamworth'),
        ('Dubbo', 'Dubbo'), ('Binnaway', 'Binnaway'),
        ('Structures', 'Structures')
    )


    type = "Item"
    title = models.CharField(max_length=150, verbose_name="Title")
    date_raised = models.DateTimeField(auto_now_add=True, verbose_name="Date raised")
    date_due = models.DateField(null=True, blank=True, verbose_name="Date due")
    description = models.TextField(verbose_name="Context", max_length=5000)
    status = models.CharField(max_length=20, choices=statuses, default=statuses[0], verbose_name="Status")
    visible = models.CharField(max_length=10, default=visibility[1], choices=visibility, verbose_name="Visible")
    actions_taken = models.TextField(max_length=5000, blank=True, default="", verbose_name="Comments")
    location = models.ForeignKey('calendar_app.Location' ,verbose_name="Location")

    purpose = models.CharField(max_length=500, blank=True, default="", verbose_name="Purpose")
    output = models.TextField(verbose_name="Output", blank=True, default="", max_length=2000)
    resources = models.TextField(verbose_name="Resources", blank=True, default="",  max_length=2000)
    addressed = models.CharField(max_length=500, blank=True, default="", verbose_name="How addressed in current plan?")
    date_closed = models.DateField(auto_now=True, verbose_name="Date closed")



    def __str__(self):
        return self.title


class Issue(Item):
    type = "Critical Question"
    raised_by = models.ForeignKey(User, verbose_name="Raised by", related_name='Issue')
    assigned_to = models.ForeignKey(User, verbose_name="Assigned to")

    def get_absolute_url(self):
        return reverse('tracker:item', args=['critical-question', self.id])


class Task(Item):
    types = (('Task', 'Task'), ('Idea', 'Idea'))
    raised_by = models.ForeignKey(User, verbose_name="Raised by", related_name='Task')
    assigned_to = models.ForeignKey(User, verbose_name="Assigned to")
    type = models.CharField(max_length=10, choices=types, default=types[0], verbose_name="Type")
    issue = models.ManyToManyField(Issue, verbose_name='Issue')

    def get_absolute_url(self):
        return reverse('tracker:item', args=['task', self.id])


class Log(models.Model):

    class Meta:
        abstract = True
        ordering = ['-when']

    what = models.CharField(max_length=100)
    when = models.DateTimeField(auto_now_add=True)
    who = models.ForeignKey(User)



class LogTask(Log):
    item = models.ForeignKey(Task)


class LogIssue(Log):
    item = models.ForeignKey(Issue)