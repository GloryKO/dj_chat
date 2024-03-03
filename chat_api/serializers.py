from rest_framework import serializers
from .models import *

class RoomSerializer(serializers.ModelSerializer):
    class Room:
        model = Room
        fields = "__all__"
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ( "room", "user", "content", "timestamp")
        read_only_fields = ("id", "timestamp")
    