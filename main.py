from fastapi import FastAPI   # type: ignore
from routes.todo_routes import todo_router
from routes.user_routes import user_router


# Create database tables
# Todo.metadata.create_all(bind=engine)  #this is used when not using alembic

app = FastAPI()




 



app.include_router(todo_router, prefix="/todos" , tags=["Todos"]) 
app.include_router(user_router, prefix="/user" , tags=["Users"]) 


# uv run alembic revision --autogenerate -m "create todos table"

# alembic upgrade head
