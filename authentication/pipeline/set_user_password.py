from django.shortcuts import redirect
from Blog.utils import send_custom_email
from authentication.models import Account, FollowersModel
from social_core.pipeline.partial import partial
from authentication.utils import add_subscriber
from django.urls.base import reverse

# partial says "we may interrupt, but we will come back here again"


@partial
def collect_password(strategy, backend, request, details, *args, **kwargs):
    # session 'local_password' is set by the pipeline infrastructure
    # because it exists in FIELDS_STORED_IN_SESSION
    local_password = strategy.session_get('local_password', None)
    user_email = kwargs['response']['email']
    user_name = kwargs['response']['given_name']
    if not local_password:
        # if we return something besides a dict or None, then that is
        # returned to the user -- in this case we will redirect to a
        # view that can be used to get a password
        return redirect("collect-password")

    # grab the user object from the database (remember that they may
    # not be logged in yet) and set their password.  (Assumes that the
    # email address was captured in an earlier step.)
    user = Account.objects.get(email=user_email)
    if not user.pwd_changed and not user.pwd_mail_sent:
        user.set_password(local_password)
        try:
            data = {
                'receiver': user_name.capitalize(),
                'password': local_password,
                'link': f"{request.scheme}://{request.get_host()}/accounts/change-password/"
            }
            send_custom_email(
                receiver_email=user_email,
                subject="Temporary Password",
                sender_email="no-reply@ireadblog.com",
                sender_name="iRead Blog",
                template_name="password.html",
                **data
            )
        except Exception as e:
            print(e)
        user.pwd_mail_sent = True
        user.save()
        FollowersModel(user=user).save()
        add_subscriber(user_email, user_name)
        data = {
            "receiver": user_name,
            'edit_profile_url': 'https://ireadblog.com' + reverse('edit_profile', args=[user.username])
        }
        print(data['edit_profile_url'])
        send_custom_email(
            receiver_email=user.email,
            subject="Welcome to iRead Blog 🎉🎉",
            sender_email="no-reply@ireadblog.com",
            sender_name="iRead Blog",
            template_name="welcome.html",
            **data
        )
    strategy.session_set('user_id', user.id)
    strategy.session_set('username', user.username)

    # continue the pipeline
    return
