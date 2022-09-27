from tortoise.contrib.pydantic import pydantic_model_creator

from models import User


UserType = pydantic_model_creator(User, name="User")
UserInType = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
