from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import UserLog, BlacklistSite
from app.schemas.logs import LogsUploadRequest
from app.api.dependencies import verify_agent

router = APIRouter()

@router.post("/logs/upload", tags=["Logs"])
def upload_logs(logs_request: LogsUploadRequest, db: Session = Depends(get_db), agent = Depends(verify_agent)):
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

    db.commit()
    return {"detail": f"{len(logs_request.logs)}개의 로그가 업로드되었습니다."}