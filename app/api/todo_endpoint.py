from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from beanie.operators import Set
from app.core.tenant_middleware import get_tenant_id
from app.core.database import mongo_client
from app.models.todo import Todo

todo_router = APIRouter(prefix="/api/todos", tags=["Todos"])

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoUpdate(TodoCreate):
    completed: bool

@todo_router.get("/", response_model=list[Todo])
async def read_todos(db = Depends(mongo_client.get_database)):
    todos = await Todo.find_all().to_list()
    return todos

@todo_router.post("/", response_model=Todo)
async def create_todo(
    new_todo: TodoCreate, 
    db = Depends(mongo_client.get_database),
    current_tenant: PydanticObjectId | None = Depends(get_tenant_id)
):
    todo = Todo(
        title=new_todo.title,
        description=new_todo.description,
        tenant_id=current_tenant
    )
    await todo.insert()
    return await Todo.get(todo.id) 

@todo_router.get("/{todo_id}", response_model=Todo)
async def read_todo(
    todo_id: PydanticObjectId, 
    db = Depends(mongo_client.get_database)
):
    todo = await Todo.find_one(Todo.id == todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    return todo

@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: PydanticObjectId, 
    db = Depends(mongo_client.get_database)
):
    todo = await Todo.find_one(Todo.id == todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    await todo.delete()
    return None

@todo_router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: PydanticObjectId, 
    updated_todo: TodoUpdate,
    db = Depends(mongo_client.get_database)
):
    todo = await Todo.find_one(Todo.id == todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    
    await todo.update(Set({
        Todo.title: updated_todo.title,
        Todo.description: updated_todo.description,
        Todo.completed: updated_todo.completed
    }))
    return await Todo.get(todo_id)
