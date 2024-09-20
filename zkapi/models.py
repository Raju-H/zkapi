from uuid import uuid4
from django.db import models

class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    ip_address = models.CharField(max_length=200)
    port = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username