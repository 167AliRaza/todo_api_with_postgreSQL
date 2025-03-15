from fastapi import APIRouter, Depends, HTTPException #type: ignore
from sqlalchemy.orm import Session #type: ignore
from config.database import get_db
from models.todo import User
from models.todo import Api_key
from validations.validation import UserCreate
from validations.validation import UserLogin
from utils.auth_util import create_access_token
from utils.auth_util import get_api_key
from utils.auth_util import verify_api_key



user_router = APIRouter()

@user_router.post("/Signup" )
def create_user(user: UserCreate, db: Session = Depends(get_db),api_key: str = Depends(get_api_key)):
    try:
        
        db_user = User( name=user.name, email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        token = create_access_token(data={"email": db_user.email, "id": db_user.id, "name": db_user.name})
        user_api = Api_key(key=api_key , user_id=db_user.id)
        db.add(user_api)
        db.commit()
        db.refresh(user_api)
        user_data = {
            "name": db_user.name,
            "email": db_user.email,
            "id": db_user.id,
            "token": token,
            "api_key": user_api.key
        
        }
        return {
        "data": user_data,
        "message": "User created successfully",
        "status": "success",
        "error": None
        }
    except Exception as e:
        return{
            "data": None,
            "error": str(e),
            "message": "An error occurred while creating the user",
            "status": "failed"}
        
        
@user_router.post("/Login" )
def login_user(user: UserLogin,api_user_id=Depends(verify_api_key) ,db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.password != user.password:
            raise HTTPException(status_code=404, detail="Invalid password")
        if db_user.id != api_user_id:
            raise HTTPException(status_code=404, detail="Invalid Api Key")
        token = create_access_token(data={"email": db_user.email, "id": db_user.id, "name": db_user.name})
        user_data = {
            "name": db_user.name,
            "email": db_user.email,
            "id": db_user.id,
            "token": token
        }
        return {
        "data": user_data,
        "message": "User logged in successfully",
        "status": "success",
        "error": None
        }
    except Exception as e:
        return{
            "data": None,
            "error": str(e),
            "message": "An error occurred while logging in the user",
            "status": "failed"}