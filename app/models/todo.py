from app.models.app_base import AppBaseModel


class Todo(AppBaseModel):
    title: str
    description: str
    completed: bool = False

    class Settings(AppBaseModel.Settings):
        name = "todos"
        
