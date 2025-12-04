from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status
from app import models
from sqlalchemy.orm import Session
from app.database import get_bd
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "secretkey") #usa .env de en produccion  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_bd)):
    credentials_exeption= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="No se puede validar el token", 
        headers={"www-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exeption
    except JWTError:
        raise credentials_exeption
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exeption
    return user