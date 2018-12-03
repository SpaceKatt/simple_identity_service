'''
This module connects us to our postgreSQL instance
'''
import os
import asyncpg as pg


async def init_db():
    '''
    Initialize our database and create a connection pool.
    '''
    user = os.environ['DB_USERNAME']
    host = os.environ['DB_HOST']
    port = os.environ['DB_PORT']
    database = os.environ['DB_DB']
    password = os.environ['DB_PASSWORD']

    return await pg.create_pool(
        database=database,
        user=user,
        host=host,
        port=port,
        password=password
    )


def get_pool(req):
    '''
    Return the connection pool from an incoming request object
    '''
    return req.app['pool']


async def insert_name_statement(req, name, password):
    '''
    Associate a statement with a fictional character
    '''
    pool = get_pool(req)

    async with pool.acquire() as connection:
        async with connection.transaction():
            try:
                await connection.execute('''
                                     INSERT INTO user (username, passhash)
                                     VALUES ($1, $2)
                                     RETURNING name_id
                                         ''', name, password)
                return True
            except pg.exceptions.UniqueViolationError:
                return False


