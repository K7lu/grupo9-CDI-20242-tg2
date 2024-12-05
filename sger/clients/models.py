from django.db import models

class Client(models.Model):

    def __str__(self):
        return self.name
