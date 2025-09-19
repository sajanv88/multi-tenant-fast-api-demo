from app.models.app_base import AppBaseModel
from beanie import Indexed

class Tenant(AppBaseModel):
    name: str = Indexed(unique=True)

    async def serialize(self):
        doc =  self.model_dump()
        base_doc = await super().serialize()
        return {
            **base_doc,
            "name": doc["name"],
        }
    class Settings(AppBaseModel.Settings):
        name = "tenants"