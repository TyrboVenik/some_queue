import logging
import random
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi import Request

from some_partner.shemas import RequestModel, ResponseModel, StatusModel

app = FastAPI()

logger = logging.getLogger(__name__)


@app.post(
    "/api/v1/application/",
    response_model=ResponseModel,
    status_code=201)
async def some_post(request: Request, payload: RequestModel):
    logger.error(payload.json())

    return ResponseModel(id=uuid.uuid4().hex)


@app.get(
    "/api/v1/application/{uid}/",
    response_model=StatusModel,
    status_code=200)
async def some_get(uid: str):
    status = 0 if random.randint(1, 10) != 2 else random.randint(20, 22)
    logger.error(uid, status)
    return StatusModel(id=uid, status=status)


if __name__ == "__main__":  # pragma: nocover
    run_dict = {
        "app": "some_partner.app:app",
        "host": "0.0.0.0",
        "port": 5000,
    }

    uvicorn.run(**run_dict)
