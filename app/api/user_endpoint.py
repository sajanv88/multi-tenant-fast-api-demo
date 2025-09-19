from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.core.tenant_middleware import extract_tenant_id_from_headers, get_tenant_id
from app.models.user import User

user_router = APIRouter(prefix="/api/users", tags=["Users"], dependencies=[extract_tenant_id_from_headers()])

class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    tenant_id: str | None = None
    created_at: str
    updated_at: str


@user_router.get("/", response_model=list[UserResponse])
async def read_users():
    users = await User.find_all().to_list()
    return [await user.serialize() for user in users]

@user_router.post("/", response_model=User)
async def create_user(
    new_user: UserCreate, 
    current_tenant: PydanticObjectId | None = Depends(get_tenant_id)
):
    user = User(
        username=new_user.username,
        email=new_user.email,
        tenant_id=current_tenant
    )
    await user.insert()
    return await User.get(user.id)


@user_router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: PydanticObjectId, 
):
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user
