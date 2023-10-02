import time

from asgiref.sync import async_to_sync

from online_computing.celery import logger
from celery import shared_task
from channels.layers import get_channel_layer
from online_computing.celery import math_computing_app

import json


@math_computing_app.task(bind=True)
def fibonacci(self, value: int, group_name=None):
    """
    this function for fibonacci pattern task
    like this ==>
    0, 1, 1, 2, 3, 5, 8, 13, ...
    and fib(n) = fib(n - 1) + fib(n - 2)
    """

    if value < 1:
        # logger warning
        logger.warning(f'this number not executing and its user input --> {value}')

        if group_name:
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'work_finality',
                    'message': json.dumps({'status': 'work_cant_executing'})
                }
            )

        return 'error'

        # raise ValueError('this number cant be less than 1')

    # set first numbers
    a, b = 0, 1

    # loop for get fib(n)
    for i in range(value):
        a, b = b, a + b

    if group_name:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'work_finality',
                'message': json.dumps({'status': 'work_ended', 'return_data': b})
            }
        )

    return b
