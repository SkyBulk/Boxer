from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.


class Messages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sender = models.ForeignKey(
        User, related_name="sender", on_delete=models.SET_NULL, null=True
    )
    receiver = models.ForeignKey(
        User, related_name="receiver", on_delete=models.SET_NULL, null=True
    )
    content = models.TextField()
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    read = models.BooleanField(default=False)
    trash = models.BooleanField(default=False)

    def __str__():
        return self.id


class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(
        User, related_name="author", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    content = models.TextField()

    def __str__():
        return self.title


class GeneralSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=1255)

    def __str__(self):
        return self.key


class VirtualMachine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    level = models.CharField(max_length=10)
    user_flag = models.CharField(min_length=32, max_length=32)
    root_flag = models.CharField(min_length=32, max_length=32)
    disk_location = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255)
    network_name = models.CharField(max_length=255)
    published = models.DateTimeField()
    user_owned = models.ManyToManyField(User, blank=True)
    root_owned = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.key
