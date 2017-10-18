from django import template
from  si_tracker.models import Item

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    else:
        return False


@register.filter('is_close_status')
def is_close_status(text):
    if isinstance(text, str):
        return text in [x[0] for x in Item.closed_statuses]
    else:
        return False