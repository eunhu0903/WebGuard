from fastapi import HTTPException, status, Header, Depends
from sqlalchemy.orm import Session
from app.db.models import User
from app.core.security import decode_access_token
from app.db.session import get_db

def get_token_from_header(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 토큰이 없거나 잘못되었습니다.")
    return authorization[7:]

def verify_token(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    email: str = payload.get("sub")

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰에 이메일 정보가 없습니다.")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 사용자입니다.")
    
    return user