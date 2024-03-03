from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    oneline_users = models.ManyToManyField(to=User, blank=True)

    def add_online_users(self,user):
        self.oneline_users.add(user)
        self.save()
    
    def remove_online_users(self,user):
        self.oneline_users.remove(user)
        

class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "chat_message"
        ordering = ("timestamp",)