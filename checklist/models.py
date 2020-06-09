from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class myList:
    def __init__(self,isshared,ishost,list_no,title,date,saveddate,savedby=None):
        self.isshared=isshared
        self.ishost=ishost
        self.list_no=list_no
        self.title=title
        self.date=date
        self.saveddate=saveddate
        self.savedby=savedby

class Item:
    def __init__(self,id,item,ischecked):
        self.id=id
        self.item=item
        self.ischecked=ischecked

class ListItems(models.Model):
    list_no = models.CharField(max_length=50)
    lastsavedon = models.DateTimeField()
    lastsavedby = models.EmailField(default=None)
    items = ArrayField(ArrayField(models.CharField(max_length=1000,blank=True),size=2))
