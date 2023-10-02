from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from .tasks import fibonacci
from online_computing.celery import math_computing_app as app

import json
import uuid


# Consumers

class MathComputing(AsyncConsumer):
    async def websocket_connect(self, event):
        self.group_name = str(uuid.uuid4())
        self.work_id = None

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'revoke_work_task',
            }
        )

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()

    async def websocket_receive(self, event):
        text_data = event.get('text', None)
        # bytes_data = event.get('bytes', None)

        if text_data:
            text_data_json = json.loads(text_data)

            text_data_option = text_data_json['option']
            text_data_value = text_data_json['value']

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'revoke_work_task',
                }
            )

            if text_data_option == 'fibonacci':
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'fibonacci',
                        'data': {
                            'text_data_value': text_data_value
                        }
                    }
                )

    async def revoke_work_task(self, event):
        if self.work_id is not None and \
                (task_async_result := app.AsyncResult(self.work_id)).state != 'SUCCESS':
            task_async_result.revoke(terminate=True)

            await self.send({
                'type': 'websocket.send',
                'text': 'one_of_your_task_was_revoked'
            })

    async def fibonacci(self, event):
        text_data_value = event['data']['text_data_value']

        res = fibonacci.apply_async([int(text_data_value), self.group_name])

        self.work_id = res.id

    async def work_finality(self, event):
        message = event['message']

        await self.send({
            'type': 'websocket.send',
            'text': message
        })
