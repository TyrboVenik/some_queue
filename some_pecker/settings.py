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

    partner_host: str


ENVS: Settings = Settings()
