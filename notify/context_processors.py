from .models import Message

def notifications(req):
    return {
        'notifications': Message.objects.filter(user=req.user, read=False).count() if req.user.is_authenticated else None
    }