from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password, get_password_hash
from app.db.session import get_db_mysql
from app.db.models import User
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse

router = APIRouter()

@router.post("/auth/signup", response_model=UserResponse, tags=["Auth"])
def signup(user: UserCreate, db: Session = Depends(get_db_mysql)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일 입니다.")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/auth/login", response_model=Token, tags=["Auth"])
def login(user: UserLogin, db: Session = Depends(get_db_mysql)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 이메일 또는 비밀번호 입니다.")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "Bearer"}