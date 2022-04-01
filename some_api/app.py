import json
import logging

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from tortoise.contrib.fastapi import register_tortoise

from some_api.db import SomeTable, TORTOISE_ORM
from some_api.rabbit import connect, QUEUE_NAME
from some_api.rabbit import send_bytes
from some_api.shemas import RequestModel, ResponseModel, QueueMessage, StatusModel

app = FastAPI()

logger = logging.getLogger(__name__)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)


@app.on_event("startup")
async def startup():
    app.state.queue_connection = await connect()


@app.on_event("shutdown")
async def shutdown():
    await app.state.queue_connection.close()


@app.post(
    "/api/v1/app/",
    response_model=ResponseModel,
    status_code=201)
async def some_post(request: Request, payload: RequestModel):
    logger.error(payload.json())
    some_row = await SomeTable.create()

    conn = request.app.state.queue_connection
    message = QueueMessage(id=some_row.pk, data=payload.data)

    await send_bytes(conn, QUEUE_NAME, json.dumps(message.dict()).encode())
    return ResponseModel(id=some_row.pk)


@app.get(
    "/api/v1/app/{app_id}/",
    response_model=StatusModel,
    status_code=200)
async def some_get(app_id: int):
    logger.error(app_id)
    some_row = await SomeTable.get_or_none(pk=app_id)
    return StatusModel(id=app_id, status=some_row and some_row.status)


if __name__ == "__main__":  # pragma: nocover
    run_dict = {
        "app": "some_api.app:app",
        "host": "0.0.0.0",
        "port": 5000,
    }

    uvicorn.run(**run_dict)
