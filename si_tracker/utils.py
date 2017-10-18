from notify.models import Message
from notify.tasks import event_user
from si_tracker.models import Issue


def message_create(msg_description, msg_item, msg_user):
    msg = Message()
    msg.description = msg_description
    if msg_item.type == Issue.type:
        msg.type_item = Message.ISSUE
        msg.item_issue = msg_item
    else:
        msg.type_item = Message.TASK
        msg.item_task = msg_item
    msg.user = msg_user
    msg.save()
    if msg.user.messageprofile.allow_email_events and msg.user.email:
        event_user(msg.id)


def message_about_task(msg_description, msg_item):
    for issue in msg_item.issue.all():
        message_create(msg_description, msg_item, issue.assigned_to)
