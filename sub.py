#!/usr/bin/env python

import asyncio
import aioamqp
import aiohttp
import asyncssh
import sys

async def curl(url):
    response = await aiohttp.request("GET", url)
    print(repr(response), file=sys.stdout)

    chunk = await response.content.read()
    print("Downloaded: %s" % len(chunk), file=sys.stdout)

    response.close()


async def run_client(command_list):
    with await asyncssh.connect('localhost') as conn:
        for cmd in command_list:
            stdin, stdout, stderr = await conn.open_session(cmd)
            output = await stdout.read()
            print(output, file=sys.stdout)
            await curl("http://127.0.0.1:8080")
            status = stdout.channel.get_exit_status()
            if status:
                print("Script finished with %d", status, file=sys.stderr)
            else:
                # print("Script finished.")
                continue


async def do_work(envelope, body):
    print("Working start ===")
    # process job here
    print(body)
    await run_client(["whoami", "sleep 5", "pwd"])
    # await asyncio.sleep(5)
    print("Working Finished ===")


async def callback(body, envelope, properties):
    loop = asyncio.get_event_loop()
    loop.create_task(do_work(envelope, body))

async def receive():
    print("start waiting receive")
    try:
        transport, protocol = await aioamqp.connect('localhost', 5672)
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    channel = await protocol.channel()
    queue_name = 'py2.queue'

    await asyncio.wait_for(channel.queue(queue_name, durable=False, auto_delete=True), timeout=10)

    await asyncio.wait_for(channel.basic_consume(queue_name, callback=callback), timeout=10)


asyncio.get_event_loop().run_until_complete(receive())
asyncio.get_event_loop().run_forever()
