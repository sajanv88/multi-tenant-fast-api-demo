from typing import Any
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  Request, Security
from app.core.database import mongo_client
from beanie import PydanticObjectId


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            request.state.tenant_id = PydanticObjectId(tenant_id)
            # Initialize the database for the tenant and initialize Beanie with tenant-specific models
            await mongo_client.init_db(f"tenant_{tenant_id}", is_tenant=True)
            
            request.state.db = await mongo_client.get_database()
        response = await call_next(request)
        return response

async def get_tenant_id(request: Request) -> PydanticObjectId | None:
    return getattr(request.state, "tenant_id", None)

def extract_tenant_id_from_headers() -> Any:
  return Security(APIKeyHeader(name="x-tenant-id", auto_error=False))

  