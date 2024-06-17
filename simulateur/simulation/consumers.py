# simulation/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SimulationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "simulation_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "simulation_updates",
            self.channel_name
        )

    async def simulation_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
