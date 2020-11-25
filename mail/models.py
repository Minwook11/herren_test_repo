from django.db import models

class Address(models.Model):
    name = models.CharField(max_length = 64, null = False)
    email = models.EmailField(unique = True)
