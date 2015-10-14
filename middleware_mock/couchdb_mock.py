#!/usr/bin/env python3
"""Basic http server with minimal setup"""

import aiohttp
import aiohttp.server
from aiohttp import web

import asyncio
from urllib.parse import urlparse, parse_qsl
from aiohttp.multidict import MultiDict
import json

f = open('couchdb_mock.json', 'r')
storage = json.load(f)
f.close()

async def read_handle(request):
    global storage
    key = request.match_info.get('key', None)
    result = json.dumps(storage.get(key))
    if not result:
        raise web.HTTPNotFound
    return web.Response(body=result.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/{key}', read_handle)

    srv = await loop.create_server(app.make_handler(),
                                        '127.0.0.1', 8080)
    print("Mocked couchdb started at http://127.0.0.1:8080")
    return srv

def main():
    global storage
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

if __name__ == '__main__':
    main()
