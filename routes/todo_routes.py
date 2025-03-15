from models.todo import Todo
from fastapi import APIRouter, Depends, HTTPException #type: ignore
from sqlalchemy.orm import Session #type: ignore

from config.database import get_db
from models.todo import Todo
from validations.validation import TodoCreate
from utils.auth_util import verify_token


todo_router = APIRouter()


# Create a new Todo
@todo_router.post("/",dependencies=[Depends(verify_token)] )

def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    try:
       
        db_todo = Todo( title=todo.title, description=todo.description)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return {
        "data": db_todo,
        "message": "Todo created successfully",
        "status": "success",
        "error": None
        }
    except Exception as e:
        return{
            "data": None,
            "error": str(e),
            "message": "An error occurred while creating the todo",
            "status": "failed"}


# Get all Todos
@todo_router.get("/",dependencies=[Depends(verify_token)])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# Get a Todo by ID
@todo_router.get("/{todo_id}" ,dependencies=[Depends(verify_token)])
def get_todo(todo_id: int,  db: Session = Depends(get_db)):
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update a Todo
@todo_router.put("/{todo_id}",dependencies=[Depends(verify_token)])
def update_todo(todo_id: int, todo_update: TodoCreate,   db: Session = Depends(get_db)):
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = todo_update.title
    todo.description = todo_update.description
    db.commit()
    db.refresh(todo)
    return todo

# Delete a Todo
@todo_router.delete("/{todo_id}",dependencies=[Depends(verify_token)])
def delete_todo(todo_id: int,  db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}

#delete all todos

@todo_router.delete("/",dependencies=[Depends(verify_token)])
def delete_all_todos(db: Session = Depends(get_db)):
    db.query(Todo).delete()
    db.commit()
    return {"message": "All Todos deleted"}