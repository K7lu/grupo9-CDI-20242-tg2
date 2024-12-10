from django.db import models

class Project(models.Model):

    def __str__(self):
        return self.name
