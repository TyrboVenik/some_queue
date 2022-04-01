from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    broker_user: str
    broker_pass: str
    broker_host: str
    broker_vhost: str

    pg_host: str
    pg_db: str
    pg_user: str
    pg_pass: str
    pg_port: str = "5432"

    message_expiration_sec: int = 10


ENVS: Settings = Settings()
