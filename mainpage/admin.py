from django.contrib import admin
from .models import Lists,DeletedList
# Register your models here.

admin.site.register(Lists)
admin.site.register(DeletedList)
