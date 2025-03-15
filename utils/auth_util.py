from fastapi import Depends,HTTPException # type: ignore
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader # type: ignore
from passlib.context import CryptContext    # type: ignore
from datetime import datetime, timedelta
from typing import Optional
import string
import secrets
import uuid
import jwt      # type: ignore 
import os
from config.database import get_db
from sqlalchemy.orm import Session # type: ignore
from models.todo import Api_key


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
API_KEY_NAME = "x-api"


api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try: 
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode,  SECRET_KEY , algorithm=ALGORITHM) # type: ignore
    except Exception as e:
        print('An exception occurred')
        print(e)
        return None
    
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        if decoded_token:
            return decoded_token
        else:
            return HTTPException(status_code=401, detail="Token not parseable")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print('An exception occurred')
        print(e)
        return HTTPException(status_code=401, detail="Invalid token")
    
def get_api_key():

    length = 32
    alphabet = string.ascii_letters + string.digits + "-_"
    api_key = ''.join(secrets.choice(alphabet) for i in range(length))
    api_key = str(uuid.uuid4()).replace('-', '')[:length//2] + ''.join(secrets.choice(alphabet) for i in range(length//2))
    return api_key

def verify_api_key(api_key_header: str = Depends(api_key_header), db: Session = Depends(get_db)) :
    try:
        # query api keys table to check if api key exists and is active, and userid match the one in the token
        # db_api_key = get_api_key(userId)
        db_api_key = db.query(Api_key).filter(Api_key.key == api_key_header).first()
        if not db_api_key:  
            raise HTTPException(status_code=401, detail="Invalid API Key")
        else:
            return db_api_key.user_id 
        
        
    except Exception as e:
      print('An exception occurred',e)
      raise HTTPException(status_code=401, detail="Invalid API Key")