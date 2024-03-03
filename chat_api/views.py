from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

class MessageList(generics.ListCreateAPIView):
    serializer_class =MessageSerializer
    queryset =Message.objects.all()
    ordering =('-timestamp')

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        if room_id:
                queryset =Message.objects.filter(room__id=room_id)
        return  queryset