from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Lists(models.Model):
    list_no = models.CharField(max_length=50)
    isshared = models.BooleanField(default=False)
    title = models.CharField(max_length=500)
    date = models.DateTimeField(default=None)
    items = ArrayField(models.CharField(max_length=1000),blank=True)

class Lists_Dates(models.Model):
    list_no = models.CharField(max_length=50)
    updatedon = models.DateTimeField()
    updatedby = models.EmailField(default=None)

class DeletedList(models.Model):
    list_no = models.CharField(max_length=50)
    delete_date = models.DateTimeField()

class MyLists(models.Model):
    email = models.EmailField()
    ishost = models.BooleanField(default=True)
    list_no = models.CharField(max_length=50)

class myList:
    def __init__(self,isshared,ishost,list_no,title,date=None,sharedwith=None,last_shared_date=None,shared_by=None):
        self.isshared=isshared
        self.ishost=ishost
        self.list_no=list_no
        self.title=title
        self.date=date
        self.sharedwith = sharedwith
        self.last_shared_date = last_shared_date
        self.shared_by=shared_by
