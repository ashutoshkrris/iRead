from django.contrib import admin
from .models import Account, FollowersModel, SocialLinks, Work
from django.contrib.auth.admin import UserAdmin
from django.urls.base import reverse
from Blog.utils import send_custom_email


@admin.action(description="Send alert to users")
def send_days_alert(modeladmin, request, queryset):
    for obj in queryset:
        data = {
            "receiver": obj.first_name,
            'edit_profile_url': 'https://ireadblog.com' + reverse('edit_profile', args=[obj.username])
        }
        send_custom_email(
            receiver_email=obj.email,
            subject="Did you forget us? 😭",
            sender_email="no-reply@ireadblog.com",
            sender_name="iRead Blog",
            template_name="days-alert.html",
            **data
        )


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    actions = (send_days_alert,)


admin.site.register(Account, AccountAdmin)
admin.site.register(SocialLinks)
admin.site.register(Work)
admin.site.register(FollowersModel)
