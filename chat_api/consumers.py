import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.room_name=None
        self.room=None
        self.room_group_name=None
        self.user =None

    #handle the wesocket connection
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user = self.scope["user"] or "anonymous"
        if not self.room_name or len(self.room_name) > 100:
            await self.close(code=400)
            return
        self.room_group_name =f"chat_{self.room_name}"
        self.room = await self.get_or_create_room() #helper function to handle room creation
        #join room
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()
        await self.create_online_user(self.user) #helper function to create user
        await self.send_user_list()

    #handle disconnection (remove room from channel layer)
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        await self.remove_online_user(self.user)
        await self.send_user_list()
    
    #handle recieveing of messages from the socket
    async def receive(self,text_data=None,bytes_data=None):
        data = json.loads(text_data)
        message = data["message"] 
        if not message or len(message) > 255:
            return 
        message_obj = await self.create_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message_obj.content,
                "username":message_obj.user.username,
                "timestamp":str(message_obj.timestaamp),
            },
        )

    #helper function to send list of connected users
    async def send_user_list(self):
        user_list = await self.get_connected_users()
        await self.channel_layer.group_send(self.room_group_name,
        {
            "type":"user_list",
            "user_list":user_list,
        }
        )

    #send the chat messages to the websocket
    async def chat_message(self,event):
        message = event["message"]
        username = event["username"]
        timestamp=event["timestamp"]
        await self.send(
            text_data=json.dumps({"message":message,"username":username,"timestamp":timestamp})
        )

   #send updated user_list to connected usrs
    async def user_list(self,event):
        user_list = event["user_list"]
        await self.send(text_data=json.dumps({"user_list":user_list}))  


    @database_sync_to_async
    def create_message(self,message):
        try:
            return Message.objects.create(room=self.room,content=message,user=self.user)
        except Exception as e :
                return None
    #handle room creation(gets or create a room)   
    @database_sync_to_async
    def get_or_create_room(self):
        room,_ =Room.objects.get_or_create(name=self.room_group_name)
        return room
    
    #creates a user
    @database_sync_to_async
    def create_online_user(self,user):
        try:
            self.room.add_online_users(user)
            self.room.save()

        except Exception as e:
            print("Error joining user to room:", str(e))
            return None
    
    #removes a user from user list
    @database_sync_to_async
    def remove_online_user(self,user):
        try:
            self.room.remove_online_users(user)
            self.room.save()
        except Exception as e :
            return None
    
    #gets the list of connected users 
    @database_sync_to_async
    def get_connected_users(self):
        return [user.username for user in self.room.online_user.all()]
