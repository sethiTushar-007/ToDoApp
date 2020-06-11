from django.contrib import admin
from .models import Lists,DeletedList,MyLists
# Register your models here.

admin.site.register(Lists)
admin.site.register(DeletedList)
admin.site.register(MyLists)
