from django.core.mail import send_mail, get_connection, EmailMessage
from simpletracker import settings

from huey.contrib.djhuey import db_periodic_task, db_task

from notify.models import Message


@db_task()
def event_user(message):
    with get_connection() as conn:
        msg = Message.objects.get(pk=message)
        item = msg.item_issue if msg.type_item == Message.ISSUE else msg.item_task
        email = EmailMessage(
            'Event: {}'.format(item.title),
            '<p>{}</p> <a href="{}{}">Item</a>'.format(msg.description, settings.SITE_URL, item.get_absolute_url()),
            settings.EMAIL_HOST_USER,
            [msg.user.email],
            connection=conn
        )
        email.content_subtype = 'html'
        email.send(fail_silently=True)


