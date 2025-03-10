from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from accounts.models import Student
from datetime import datetime
# Create your models here.

class Room(models.Model):
    participants=models.ManyToManyField(User,related_name="room")
    name = models.CharField(max_length=2000)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"room entre {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now , blank = True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
