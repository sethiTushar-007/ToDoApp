from django.db import models

# Create your models here.
class myList:
    def __init__(self,isshared,ishost,list_no,title,createdon,createdby=None,updatedon=None,updatedby=None):
        self.isshared=isshared
        self.ishost=ishost
        self.list_no=list_no
        self.title=title
        self.createdon=createdon
        self.createdby = createdby
        self.updatedon=updatedon
        self.updatedby = updatedby


class myItem:
    def __init__(self,id,item,isFirst=False,isLast=False):
        self.id=id
        self.item=item
        self.isFirst=isFirst
