from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_bd
from app import models, schemas
from app.utils import hash_password, verify_password, create_access_token
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
def auth_status():
    return {"status": "Auth funcionando"}

@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session= Depends(get_bd)):
    #Verificamos si el usuario existe
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya existente")

    hashed_pw= hash_password(user.password)
    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(email: str, password: str, db: Session=Depends(get_bd)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")

    access_token = create_access_token(data={"sub":user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
