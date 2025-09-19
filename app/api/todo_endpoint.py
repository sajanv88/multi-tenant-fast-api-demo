from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from beanie.operators import Set
from app.core.tenant_middleware import extract_tenant_id_from_headers, get_tenant_id
from app.models.todo import Todo

todo_router = APIRouter(prefix="/api/todos", tags=["Todos"], dependencies=[extract_tenant_id_from_headers()])

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoUpdate(TodoCreate):
    completed: bool

class TodoResponse(TodoCreate):
    id: str
    tenant_id: str | None = None
    completed: bool
    created_at: str
    updated_at: str

@todo_router.get("/", response_model=list[TodoResponse])
async def read_todos():
    todos = await Todo.find_all().to_list()
    return [await todo.serialize() for todo in todos]

@todo_router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    new_todo: TodoCreate, 
    current_tenant: PydanticObjectId | None = Depends(get_tenant_id)
):
    todo = Todo(
        title=new_todo.title,
        description=new_todo.description,
        tenant_id=current_tenant
    )
    await todo.insert()
    return await todo.serialize()

@todo_router.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(
    todo_id: PydanticObjectId
):
    todo = await Todo.find_one(Todo.id == todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    return await todo.serialize()

@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: PydanticObjectId
):
    todo = await Todo.find_one(Todo.id == todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    await todo.delete()
    return None

@todo_router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: PydanticObjectId, 
    updated_todo: TodoUpdate,
):
    todo = await Todo.find_one(Todo.id == todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    
    await todo.update(Set({
        Todo.title: updated_todo.title,
        Todo.description: updated_todo.description,
        Todo.completed: updated_todo.completed
    }))
    return await todo.serialize()
