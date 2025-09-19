from datetime import datetime, timezone
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import ConfigDict, Field

class AppBaseModel(Document):
    model_config = ConfigDict(
        json_encoders={PydanticObjectId: str},
    )
    tenant_id: Optional[PydanticObjectId] = None
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    updated_at: datetime = Field(default=datetime.now(timezone.utc))

    class Settings:
        indexes = [
            "tenant_id",
            [("tenant_id", 1), ("created_at", -1)],
        ]
