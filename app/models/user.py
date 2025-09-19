from beanie import  Indexed, PydanticObjectId

from pydantic import EmailStr, Field, ConfigDict

from app.models.app_base import AppBaseModel


class User(AppBaseModel):
  

    username: str
    email: EmailStr = Indexed(EmailStr, unique=True)

    async def serialize(self):
        doc =  self.model_dump()
        base_doc = await super().serialize()
        return {
            **base_doc,
            "username": doc["username"],
            "email": doc["email"],
        }


    class Settings(AppBaseModel.Settings):
        name = "users"
