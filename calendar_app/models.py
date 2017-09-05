from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User



class Location(models.Model):

    name = models.CharField(verbose_name="Location name", max_length=100)
    parent = models.ForeignKey("self", blank=True, null=True, verbose_name="Parent location",)
    owner = models.ForeignKey(User, blank=True, null=True, verbose_name="Owner", related_name='Location')
    members = models.ManyToManyField(User, blank=True, null=True, verbose_name="Members")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("calendar:location_detail", args=[self.id])


class Event(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    date = models.DateTimeField(verbose_name="Date")

    def __str__(self):
        return self.name


