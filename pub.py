#!/usr/bin/env python

import asyncio
import aioamqp
import json


async def produce():
    try:
        transport, protocol = await aioamqp.connect('localhost', 5672)
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    queue_name = 'taas.test_queue'
    channel = await protocol.channel()
    await asyncio.wait_for(channel.queue(queue_name, durable=False, auto_delete=True), timeout=10)
    data = {"id": "11111"}
    await channel.publish(json.dumps(data), '', queue_name)
    print("Pushed")

    await protocol.close()

asyncio.get_event_loop().run_until_complete(produce())
