from . import views
from django.urls import path

urlpatterns = [
    path('chat/rooms/<int:room_id>/messages/', views.MessageList.as_view(), name='chat-messages'),
]