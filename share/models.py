from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Sharing(models.Model):
    sharedto = models.EmailField()
    list_no = models.CharField(max_length=50)
    sharedon = models.DateTimeField()
    host = models.EmailField()

class Share:
    def __init__(self,id,person,isFirst=False,isLast=False):
        self.id=id
        self.person=person
        self.isFirst=isFirst
