from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User,auth
from allauth.account.models import EmailAddress

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self,request,sociallogin):
        if sociallogin.is_existing:
            return super(SocialAccountAdapter,self).pre_social_login(request,sociallogin)
        else:
            if User.objects.filter(username=email).exists():
                User.objects.filter(username=email).delete()
                return super(SocialAccountAdapter,self).pre_social_login(request,sociallogin)
