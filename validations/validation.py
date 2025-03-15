from pydantic import BaseModel      # type: ignore

# Pydantic model for validation
class TodoCreate(BaseModel):
    title: str
    description: str  # type: 
    
class UserCreate(BaseModel):
    email: str
    name: str
    password: str 
    
class UserLogin(BaseModel):
    email: str
    password: str 
    
    
    