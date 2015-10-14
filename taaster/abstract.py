#!/usr/bin/env python

"""
Abstract Tester Class
"""

import asyncio

class AbstractTester(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in dir(self):
                setattr(self, k, v)
        return super().__init__()


    async def before_job(self):
        pass

    def do_job(self):
        pass

    async def after_job(self):
        pass

    def run_forever(self, *args, **kwargs):
        ioloop = asyncio.get_event_loop()
        asyncio.ensure_future(self.before_job())
        self.do_job()
        asyncio.ensure_future(self.after_job())

