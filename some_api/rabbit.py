import asyncio

import aio_pika
from aio_pika import Connection

from some_api.settings import ENVS

QUEUE_URL = f"amqp://{ENVS.broker_user}:{ENVS.broker_pass}@{ENVS.broker_host}/{ENVS.broker_vhost}"
QUEUE_NAME = f'some_queue_name'


async def connect() -> Connection:
    conn = await aio_pika.connect_robust(QUEUE_URL, loop=asyncio.get_event_loop())

    async with conn.channel() as channel:
        await channel.declare_queue(QUEUE_NAME)

    return conn


async def send_bytes(conn: Connection, routing_key: str, message: bytes):
    async with conn.channel() as channel:
        await channel.default_exchange.publish(
            aio_pika.Message(body=message, expiration=ENVS.message_expiration_sec),
            routing_key=routing_key,
        )
