import json
import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async

from acc.connection import run_command_list
from .models import Command

@sync_to_async
def get_command_list(com_id_list):
     com_list = []
     for com_id in com_id_list:
          com_list.append(Command.objects.get(pk=com_id).command)
     return com_list

class RunCommandsOnNE(AsyncJsonWebsocketConsumer):
     async def connect(self):
          await self.accept()

     async def receive(self, text_data=None, bytes_data=None, **kwargs):
          data = json.loads(text_data)
          com_id_list = data.get('id_list')
          com_list = await get_command_list(com_id_list)
          output = run_command_list(data['ip'], data['login'], 
                                    data['password'], com_list)
          while True:
               try:
                    out = output.__next__()
                    if out.get('status'):
                         ne_name = out.get('status').split()[-1]
                         out.update({'ne': ne_name})
                    await self.send_json(out)
                    await asyncio.sleep(0.2)
               except ConnectionError:
                    await self.send_json({'status': f'Failed connect to {data["ip"]}'})
                    break
               except StopIteration:
                    await self.send_json({'status': f'{ne_name} checked!'})
                    break
                    
          