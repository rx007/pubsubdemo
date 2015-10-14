#!/usr/bin/env python

"""
queue.py
Mixin for Abstract Tester.

Tester will subscribe to a queue, getting job and do it.
"""
import asyncio
import aioamqp

class QueueMixin:
    pass


class AMQPQueueMixin(QueueMixin):

    amqp_host = "localhost"
    amqp_port = 5672
    amqp_queue = "taas.test_queue"

    async def before_job(self):
        try:
            transport, protocol = await aioamqp.connect(
                    self.amqp_host, self.amqp_port)
        except aioamqp.AmqpClosedConnection:
            self.logger.info("closed connections")
            return

        channel = await protocol.channel()

        await asyncio.wait_for(
                channel.queue(
                    self.amqp_queue, 
                    durable=False, 
                    auto_delete=True
                    ), 
                timeout=10
                )

        await asyncio.wait_for(
                channel.basic_consume(
                    self.amqp_queue, 
                    callback=self.job_callback), 
                timeout=10
                )

    def do_job(self):
        asyncio.get_event_loop().run_forever()

    async def job_callback(self, body, envelope, properties, *args, **kwargs):
        pass

