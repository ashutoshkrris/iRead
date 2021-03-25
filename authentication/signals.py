from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Account, FollowersModel

@receiver(m2m_changed, sender=FollowersModel.following.through)
def add_follower(sender, instance, action, reverse, pk_set, **kwargs):
    """Add follower signal

    Args:
        sender ([type]): model which will send signal (following)
        instance ([type]): username of user who is logged in (session user)
        action ([type]): pre_add if suer followed someone else pre_remove if user unfollowed someone
        reverse ([type]): false
        pk_set ([type]): id set of all users followed by logged in user
    """

    followed = [] # list of followed users
    logged_in_user = Account.objects.get(email=instance)
    for i in pk_set:
        user = Account.objects.get(id=i)
        following_obj = FollowersModel.objects.get(user=user)
        followed.append(following_obj)

    if action == 'pre_add':
        for i in followed:
            i.follower.add(logged_in_user)
            i.save()

    if action == 'pre_remove':
        for i in followed:
            i.follower.remove(logged_in_user)
            i.save()
