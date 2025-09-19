from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.core.tenant_middleware import get_tenant_id
from app.core.database import mongo_client
from app.models.user import User

user_router = APIRouter(prefix="/api/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str
    email: EmailStr


@user_router.get("/", response_model=list[User])
async def read_users(db = Depends(mongo_client.get_database)):
    users = await User.find_all().to_list()
    return users

@user_router.post("/", response_model=User)
async def create_user(
    new_user: UserCreate, 
    db = Depends(mongo_client.get_database),
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
    db = Depends(mongo_client.get_database)
):
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user
