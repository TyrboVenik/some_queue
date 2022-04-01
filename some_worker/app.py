import asyncio
import json
import logging

import aio_pika
import requests
from aio_pika import Connection
from tortoise import Tortoise

from some_worker.db import SomeTable, TORTOISE_ORM
from some_worker.settings import ENVS

QUEUE_URL = f"amqp://{ENVS.broker_user}:{ENVS.broker_pass}@{ENVS.broker_host}/{ENVS.broker_vhost}"
QUEUE_NAME = f'some_queue_name'
QUEUE_PECKER_NAME = f'some_pecker_queue_name'

logger = logging.getLogger(__name__)


async def send_bytes(conn: Connection, routing_key: str, message: bytes):
    async with conn.channel() as channel:
        await channel.default_exchange.publish(
            aio_pika.Message(body=message),
            routing_key=routing_key,
        )


async def main():
    logger.error("Start")

    await Tortoise.init(config=TORTOISE_ORM)

    conn = await aio_pika.connect_robust(QUEUE_URL, loop=asyncio.get_event_loop())

    async with conn:
        channel = await conn.channel()
        queue = await channel.declare_queue(QUEUE_NAME)
        await channel.declare_queue(QUEUE_PECKER_NAME)
        async for message in queue:
            async with message.process():
                try:
                    decoded_message = json.loads(message.body.decode())
                    logger.error(decoded_message)

                    r = requests.post(
                        f"{ENVS.partner_host}/api/v1/application/",
                        json={"data": decoded_message["data"]},
                    )
                    logger.error(f"{r.status_code=}")
                    r_json = r.json()
                    await SomeTable.filter(pk=decoded_message["id"]).update(status=1)
                    logger.error(r_json)
                    await send_bytes(
                        conn,
                        QUEUE_PECKER_NAME,
                        json.dumps({"uid": r_json["id"], "id": decoded_message["id"]}).encode(),
                    )
                    logger.error("SEND")
                except Exception:
                    logger.exception("похуй")

if __name__ == "__main__":
    asyncio.run(main())
