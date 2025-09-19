from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from app.core.database import mongo_client
from app.api.user_endpoint import user_router
from app.api.todo_endpoint import todo_router
from app.api.tenant_endpoint import tenant_router
from app.core.tenant_middleware import TenantMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # initialization database with application-wide models Typically the host database
    await mongo_client.init_db("app_db", is_tenant=False)
    yield
    # Shutdown code
    await mongo_client.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(TenantMiddleware)

router = APIRouter(prefix="/api/v1")


@app.get("/")
async def read_root():
    return {"Hello": "World"}

router.include_router(user_router)
router.include_router(todo_router)
router.include_router(tenant_router)

app.include_router(router)