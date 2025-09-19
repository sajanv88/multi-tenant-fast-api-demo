from typing import Sequence
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from beanie import Document, UnionDoc, View, init_beanie

from app.config import Configuration
from app.models.tenant import Tenant
from app.models.todo import Todo
from app.models.user import User


class Database:
    def __init__(self, uri: str, models: Sequence[type[Document] | type[UnionDoc] | type[View] | str] | None = None) -> None:
        self.client = AsyncMongoClient(uri)
        self.models = models

    async def init_db(self, db_name: str, is_tenant: bool | None) -> None:
        self.db: AsyncDatabase = self.client[db_name]
        if self.models:
            if is_tenant:
                tenant_models = [model for model in self.models if model != Tenant]
                await init_beanie(self.db, document_models=tenant_models)
            else:
                await self.init_models()

    async def init_models(self) -> None:
        await init_beanie(self.db, document_models=self.models)

    async def get_database(self) -> AsyncDatabase:
        return self.db

    async def close(self) -> None:
        await self.client.close()

config = Configuration()
print(f"Mongo URI: {config.mongo_uri}")
mongo_client = Database(config.mongo_uri, models=[User, Todo, Tenant])
