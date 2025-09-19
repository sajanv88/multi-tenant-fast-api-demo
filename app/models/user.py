from beanie import Document, Indexed

from pydantic import EmailStr

from app.models.app_base import AppBaseModel


class User(AppBaseModel):
    username: str
    email: EmailStr = Indexed(EmailStr, unique=True)

    class Settings(AppBaseModel.Settings):
        name = "users"
