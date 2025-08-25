from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db_pg
from app.db.models import UserLog, BlacklistSite
from app.schemas.logs import LogsUploadRequest
from app.api.dependencies import verify_agent

router = APIRouter()

@router.post("/logs/upload", tags=["Logs"])
def upload_logs(logs_request: LogsUploadRequest, db: Session = Depends(get_db_pg), agent = Depends(verify_agent)):
    saved_count = 0
    for log in logs_request.logs:
        site = db.query(BlacklistSite).filter(BlacklistSite.domain == log.site_domain).first()
        if not site:
            continue

        new_log = UserLog(
            user_id=None,
            site_id=site.id,
            attempted_at=log.attempted_at,
            action=log.action,
        )
        db.add(new_log)
        saved_count += 1

    db.commit()
    return {"detail": f"{saved_count}개의 로그가 PostgreSQL에 업로드되었습니다."}