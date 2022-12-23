from django.db import models

class connexionInformation(models.Model):
    username = models.CharField("userName", max_length=200)
    password = models.CharField(max_length=200)
