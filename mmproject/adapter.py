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


            return u.email.split('@')[1] == "mahna.co.jp"

        elif u.email.split('@')[1] == "gmail.com":
            u.is_active = False
            u.outside = True

            return u.email.split('@')[1] == "gmail.com"