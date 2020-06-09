from django.contrib import admin
from .models import PendingEmailsVerify,PasswordEmailVerify
# Register your models here.
admin.site.register(PendingEmailsVerify)
admin.site.register(PasswordEmailVerify)

