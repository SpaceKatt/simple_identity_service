'''
Runs the webserver.
'''

# External dependencies
# import aiofiles
import asyncio
# import json

from aiohttp import web

from .db import pg_cli

# built-in dependencies
# import traceback
# import io

# from gzip import GzipFile
# from urllib.parse import urlparse
# from os import path


ROUTES = web.RouteTableDef()


@ROUTES.get('/')
async def root_handle(req):
    '''
    Tells the malcontent to go root themselves off our lawn.
    '''
    return web.Response(status=200, body='Stuff goes here')


async def init_app():
    '''
    Initialize the database, then application server
    '''
    app = web.Application()

    app['pool'] = await pg_cli.init_db()

    app.add_routes(ROUTES)

    return app


LOOP = asyncio.get_event_loop()
APP = LOOP.run_until_complete(init_app())


if __name__ == '__main__':
    web.run_app(APP, host='0.0.0.0:8080')
