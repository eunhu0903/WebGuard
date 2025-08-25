from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db_mysql, get_db_pg
from app.service.sync import sync_blacklist

router = APIRouter()

@router.post("/sync/blacklist", tags=["Sync"])
def sync_blacklist_endpoint(
    mysql_db: Session = Depends(get_db_mysql),
    pg_db: Session = Depends(get_db_pg)
):
    count = sync_blacklist(mysql_db, pg_db)
    return {"detail": f"{count}개의 블랙리스트 도메인이 PostgreSQL로 동기화되었습니다."}