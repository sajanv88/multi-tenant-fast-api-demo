from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  Request
from app.core.database import mongo_client
from beanie import PydanticObjectId

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            request.state.tenant_id = PydanticObjectId(tenant_id)
            await mongo_client.init_db(f"tenant_{tenant_id}")
            
            request.state.db = await mongo_client.get_database()
        response = await call_next(request)
        return response

async def get_tenant_id(request: Request) -> PydanticObjectId | None:
    return getattr(request.state, "tenant_id", None)