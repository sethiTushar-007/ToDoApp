from django.db import models

# Create your models here.
class PendingEmailsVerify(models.Model):
    no = models.CharField(max_length=100)
    fname = models.CharField(max_length=50)
    password = models.CharField(max_length=10,default="none")
    email = models.EmailField()

class PasswordEmailVerify(models.Model):
    no = models.CharField(max_length=100)
    email = models.EmailField()