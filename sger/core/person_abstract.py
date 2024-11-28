from abc import ABC, abstractmethod
from django.db import models

class PersonAbstract(models.Model, ABC):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    class Meta:
        abstract = True

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_contact(self):
        pass

    def __str__(self):
        return self.name
