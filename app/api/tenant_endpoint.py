from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from beanie import PydanticObjectId
from app.models.tenant import Tenant


tenant_router = APIRouter(prefix="/tenants", tags=["Tenants"])

class TenantCreate(BaseModel):
    name: str

class TenantResponse(BaseModel):
    id: str
    name: str
    created_at: str
    updated_at: str

@tenant_router.get("/", response_model=list[TenantResponse])
async def read_tenants():
    tenants = await Tenant.find_all().to_list()
    return [await tenant.serialize() for tenant in tenants]


@tenant_router.post("/", response_model=TenantResponse, status_code=201)
async def create_tenant(tenant: TenantCreate):
    tenant = Tenant(name=tenant.name)
    await tenant.insert()
    return await tenant.serialize()

@tenant_router.get("/{tenant_id}", response_model=TenantResponse)
async def read_tenant(tenant_id: PydanticObjectId):
    tenant = await Tenant.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return await tenant.serialize()

@tenant_router.delete("/{tenant_id}", status_code=204)
async def delete_tenant(tenant_id: PydanticObjectId):
    tenant = await Tenant.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    await tenant.delete()
    return None