import json
import aiohttp
import asyncio
import worker
import pub
import middleware_mock.logapi_mock
import unittest

class TestWorker(unittest.TestCase):

    async def put_data(self, data):
        response = aiohttp.request("PUT", "http://localhost:8081/log/1", data=data)
        d = await response
        t = await d.read()
        response.close()
        return t
        
    async def get_data(self):
        response = aiohttp.request("GET", "http://localhost:8081/log/1")
        d = await response
        t = await d.read()
        response.close()
        return t

    def test_pushjob(self):
        loop = asyncio.get_event_loop()
        # 1. setup logapi
        loop.run_until_complete(middleware_mock.logapi_mock.init(loop))

        # 2. send a data to logapi
        data = json.dumps({
                "id": "1",
                "tasks": {
                    "ssh_host": "localhost",
                    "ssh_port": 22,
                    "ssh_username": "zhaomeng",
                    "ssh_password": "19860729",
                    "script": [
                        "whoami",
                        "pwd",
                        "which python"
                    ]
                }
        })
        task2 = asyncio.ensure_future( self.put_data(data))
        task3 = asyncio.ensure_future( self.get_data())

        # 3. awake worker
        w = worker.TaasWorker()
        task4 = asyncio.ensure_future(w.do_work("1"))
        
        loop.run_until_complete(asyncio.wait([task2, task3, task4]))
        # loop.run_forever()

        print("FINAL")
        loop.run_until_complete(self.get_data())

if __name__ == '__main__':
    unittest.main()
