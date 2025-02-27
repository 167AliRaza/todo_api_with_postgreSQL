from fastapi import FastAPI, Depends, HTTPException    # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from config.database import SessionLocal, engine
from models.todo import Todo
from pydantic import BaseModel      # type: ignore
from typing import List

# Create database tables
Todo.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for validation
class TodoCreate(BaseModel):
    title: str
    description: str  # type: ignore
 

# Create a new Todo
@app.post("/todos/" )

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
@app.get("/todos/")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# Get a Todo by ID
@app.get("/todos/{todo_id}" )
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update a Todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo_update: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = todo_update.title
    todo.description = todo_update.description
    db.commit()
    db.refresh(todo)
    return todo

# Delete a Todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}


# uv run alembic revision --autogenerate -m "create todos table"

# alembic upgrade head
@app.delete("/todos")
def delete_all_todos(db: Session = Depends(get_db)):
    db.query(Todo).delete()
    db.commit()
    return {"message": "All Todos deleted"}