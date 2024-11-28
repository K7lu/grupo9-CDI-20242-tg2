from abc import ABC, abstractmethod
from django.db import models

class EntityWithProjectAbstract(models.Model, ABC):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        abstract = True

    @abstractmethod
    def get_details(self):
        pass
