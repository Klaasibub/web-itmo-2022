from fastapi import FastAPI

from tortoise import fields, models
from tortoise.contrib.fastapi import register_tortoise

from settings import DB_URL


class User(models.Model):
    """
    The User model
    """
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=25, unique=True)
    password = fields.CharField(max_length=128, null=True)
    creation_date = fields.DatetimeField(auto_now_add=True)
    last_modified = fields.DatetimeField(auto_now=True)

    class PydanticMeta:
        exclude = ["creation_date", "last_modified"]


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
