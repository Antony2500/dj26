import uuid
from django.db import models


class GoITeeens(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.IntegerField(default=0, null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(blank=True, null=False)