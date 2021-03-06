from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class MessageProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='messageprofile')
    allow_email_events = models.BooleanField(default=True, verbose_name='Receive notification emails?')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        MessageProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.messageprofile.save()

