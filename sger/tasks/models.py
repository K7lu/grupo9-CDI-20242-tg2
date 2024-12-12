from django.db import models

class Task(models.Model):

    def __str__(self):
        return self.name
