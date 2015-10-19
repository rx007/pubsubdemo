#!/usr/bin/env python3
"""Basic http server with minimal setup"""

import aiohttp
import aiohttp.server
from aiohttp import web

import asyncio
from urllib.parse import urlparse, parse_qsl
from aiohttp.multidict import MultiDict
import json

storage = {}


async def get_log(request):
    global storage
    key = request.match_info.get("key")
    result = json.dumps(storage.get(key, {}))
    return web.Response(body=result.encode('utf-8'))

# async def post_log(request):
#     global storage
#     body = await request.read()
#     key = str(len(storage.keys()) + 1)
#     storage[key] = json.loads(body.decode('utf-8'))
#     json.dumps(storage.get(key, {}))
#     result = json.dumps({"result": "ok", "id": key})
#     return web.Response(body=result.encode('utf-8'))

async def post_log(request):
    global storage
    key = request.match_info.get("key")
    body = await request.read()
    storage[key] = json.loads(body.decode('utf-8'))
    json.dumps(storage.get(key, {}))
    result = json.dumps({"result": "ok", "id": key})
    return web.Response(body=result.encode('utf-8'))

async def delete_log(request):
    global storage
    key = request.match_info.get("key")
    del storage[key]
    result = json.dumps({"result": "ok", "id": key})
    return web.Response(body=result.encode('utf-8'))

async def log_handle(request):

    method = str(request.method)
    if method == "GET":
        res = await get_log(request)
        return res

    if method == "POST":
        res = await post_log(request)
        return res

    if method == "DELETE":
        res = await delete_log(request)
        return res

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/log/{key}', log_handle)
    app.router.add_route('POST', '/log/', log_handle)
    app.router.add_route('POST', '/log/{key}', log_handle)
    app.router.add_route('DELETE', '/log/{key}', log_handle)

    srv = await loop.create_server(app.make_handler(),
                                        '127.0.0.1', 8081)
    print("Mocked logapi started at http://127.0.0.1:8081")
    return srv

def main():
    global storage
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

if __name__ == '__main__':
    main()

