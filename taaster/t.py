import asyncio

class Tester(object):

    async def work(self):
        print("Working...")
        await asyncio.sleep(5)
        print("Work finished.")
        

ioloop = asyncio.get_event_loop()

t = Tester()

ioloop.run_until_complete(t.work())

