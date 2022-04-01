from tortoise import Model, fields

from some_api.settings import ENVS

db_url = f"postgres://{ENVS.pg_user}:{ENVS.pg_pass}@{ENVS.pg_host}:{ENVS.pg_port}/{ENVS.pg_db}"

TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "app": {
            "models": ["some_api.db"],
        },
    },
}


class SomeTable(Model):
    status = fields.IntField(default=0)
