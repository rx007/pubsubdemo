#!/usr/bin/env python

import asyncio
import aioamqp


async def produce():
    try:
        transport, protocol = await aioamqp.connect('localhost', 5672)
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    queue_name = 'py2.queue'
    channel = await protocol.channel()
    await asyncio.wait_for(channel.queue(queue_name, durable=False, auto_delete=True), timeout=10)

    # while True:
    await channel.publish("py3.message", '', queue_name)
    print("Pushed")
    # await asyncio.sleep(10)
    return


asyncio.get_event_loop().run_until_complete(produce())
