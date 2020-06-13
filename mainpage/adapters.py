from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User,auth
from django.contrib import messages

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self,request,sociallogin):
        if sociallogin.is_existing:
            return super(SocialAccountAdapter,self).pre_social_login(request,sociallogin)
        else:
            email = sociallogin.account.extra_data['email'].lower()
            if User.objects.filter(username=email).exists():
                User.objects.filter(username=email).delete()
                messages.info(request,'Now you are connected with your google account - '+email)
                return super(SocialAccountAdapter,self).pre_social_login(request,sociallogin)
            return super(SocialAccountAdapter,self).pre_social_login(request,sociallogin)
    def social_account_added(self,request,sociallogin):
        email = sociallogin.account.extra_data['email'].lower()
        if User.objects.filter(username=email).exists():
            user = User.objects.filter(username=email)[0]
            user.first_name = sociallogin.account.extra_data['name']
            user.last_name = sociallogin.account.extra_data['picture']
            user.save()
        return super(SocialAccountAdapter,self).social_account_added(request,sociallogin)
    def social_account_updated(self,request,sociallogin):
        email = sociallogin.account.extra_data['email'].lower()
        if User.objects.filter(username=email).exists():
            user = User.objects.filter(username=email)[0]
            user.first_name = sociallogin.account.extra_data['name']
            user.last_name = sociallogin.account.extra_data['picture']
            user.save()
        return super(SocialAccountAdapter,self).social_account_updated(request,sociallogin)