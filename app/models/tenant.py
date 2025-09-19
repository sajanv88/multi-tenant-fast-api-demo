from app.models.app_base import AppBaseModel


class Tenant(AppBaseModel):
    name: str

    class Settings(AppBaseModel.Settings):
        name = "tenants"