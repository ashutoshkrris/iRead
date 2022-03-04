from django import template
from core.models import Notification
from authentication.models import Account
import readtime


register = template.Library()


@register.inclusion_tag('partials/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = Account.objects.get(
        id=context['request'].session['user_id'])
    notifications = Notification.objects.filter(
        to_user=request_user).exclude(user_has_seen=True).order_by('-timestamp')
    return {'notifications': notifications}


@register.filter('readtime')
def read(html):
    return readtime.of_html(html)


@register.filter('humanize_views')
def humanize_views(views):
    str_views = len(str(views))
    if str_views <= 3:
        return views
    elif str_views <= 6:
        return f"{round(views/1000,1)}K"
    elif str_views <= 9:
        return f"{round(views/1000000, 1)}M"
    else:
        return f"{round(views/1000000000,1)}B"
