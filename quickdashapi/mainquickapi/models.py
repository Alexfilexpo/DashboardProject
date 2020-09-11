from datetime import datetime
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    entry_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    total_quota = models.PositiveIntegerField(default=0)
    total_hours_analysed = models.PositiveIntegerField(default=0)
    ceretai_user = models.BooleanField(default=False)
    test_user = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    current_quota = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)


class Entries(models.Model):
    video_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    external_id = models.PositiveIntegerField(unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)
    project = models.CharField(max_length=255)
