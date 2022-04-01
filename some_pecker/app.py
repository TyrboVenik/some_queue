import asyncio
import json
import logging

import aio_pika
import requests
from tortoise import Tortoise

from some_pecker.db import SomeTable, TORTOISE_ORM
from some_pecker.settings import ENVS

QUEUE_URL = f"amqp://{ENVS.broker_user}:{ENVS.broker_pass}@{ENVS.broker_host}/{ENVS.broker_vhost}"
QUEUE_NAME = "some_pecker_queue_name"

logger = logging.getLogger(__name__)


async def main():
    logger.error("Start")

    await Tortoise.init(config=TORTOISE_ORM)

    conn = await aio_pika.connect_robust(QUEUE_URL, loop=asyncio.get_event_loop())

    async with conn:
        channel = await conn.channel()
        queue = await channel.declare_queue(QUEUE_NAME)
        async for message in queue:
            async with message.process():
                try:
                    decoded_message = json.loads(message.body.decode())
                    logger.error(decoded_message)
                    status = 0
                    while not status:
                        r = requests.get(
                            f"{ENVS.partner_host}/api/v1/application/{decoded_message['uid']}/",
                        )
                        logger.error(f"{r.status_code=}")
                        r_json = r.json()

                        status = r_json["status"]
                        logger.error(f"{status=}")

                    await SomeTable.filter(pk=decoded_message["id"]).update(status=status)
                    logger.error(r_json)
                except Exception:
                    logger.exception("похуй")


if __name__ == "__main__":
    asyncio.run(main())
