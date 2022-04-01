from tortoise import Model, fields

from some_pecker.settings import ENVS

db_url = f"postgres://{ENVS.pg_user}:{ENVS.pg_pass}@{ENVS.pg_host}:{ENVS.pg_port}/{ENVS.pg_db}"

TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "app": {
            "models": ["some_pecker.db"],
        },
    },
}


class SomeTable(Model):
    status = fields.IntField(default=0)
