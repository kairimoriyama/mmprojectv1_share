from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False # No email/password signups allowed

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        u = sociallogin.user

        if u.email.split('@')[1] == "mahna.co.jp":
            u.is_active = True
            u.is_staff = False

            # グループ
            group = Group.objects.get(name='mahna_staff')
            user.groups.add(group)

            return u.email.split('@')[1] == "mahna.co.jp"

        elif u.email.split('@')[1] == "gmail.com":
            sociallogin.user.is_active = False
            sociallogin.user.is_staff = False
            return u.email.split('@')[1] == "gmail.com"