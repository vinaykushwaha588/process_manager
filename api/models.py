from django.db import models
import uuid

class BaseUUID(models.Model):
    """
        Abstract base model providing UUID as primary key and
        timestamp fields for creation and updates.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class System(BaseUUID):
    """
        Represents a system with a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Process(BaseUUID):
    """
        Represents a process running on a system with various attributes.
    """
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="processes")
    pid = models.IntegerField()
    name = models.CharField(max_length=255)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{}-{}".format(self.system.name, self.pid)
    