import json
import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async

from atn.connection import run_command_list as huawei_rcl
from n3com.connection import run_command_list as n3com_rcl
from .models import Command
from .models import Device


@sync_to_async
def choose_dev(vendor):
     match vendor:
        case 'huawei':
           return huawei_rcl
        case 'n3com':
            return n3com_rcl

@sync_to_async
def get_command_list(com_id_list):
     com_list = []
     for com_id in com_id_list:
          com_list.append(Command.objects.get(pk=com_id))
     return com_list


class RunCommandsOnNE(AsyncJsonWebsocketConsumer):
     async def connect(self):
          await self.accept()

     async def receive(self, text_data=None, bytes_data=None, **kwargs):
          data = json.loads(text_data)
          com_id_list = data.get('id_list')
          com_list = await get_command_list(com_id_list)
          run_command_list = await choose_dev(data.get('vendor'))
          output = run_command_list(data['ip'], data['login'], 
                                    data['password'], data['iplist'], com_list)
          while True:
               try:
                    out = await anext(output)
                    if out.get('status'):
                         ne_name = out.get('status').split()[-1]
                         out.update({'ne': ne_name})
                    await self.send_json(out)
                    await asyncio.sleep(0.1)
               except ConnectionError:
                    await self.send_json({'status': f'Не удалось подключиться к {data["ip"]}'})
                    break
               except StopAsyncIteration:
                    await self.send_json({'status': f'{ne_name} проверен!'})
                    break
                    
          