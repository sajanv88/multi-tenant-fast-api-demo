from app.models.app_base import AppBaseModel


class Todo(AppBaseModel):
    title: str
    description: str
    completed: bool = False

    async def serialize(self):
        doc =  self.model_dump()
        base_doc = await super().serialize()
        return {
            **base_doc,
            "title": doc["title"],
            "description": doc["description"],
            "completed": doc["completed"],
        }
    class Settings(AppBaseModel.Settings):
        name = "todos"
        
