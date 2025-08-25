from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db_mysql
from app.db.models import BlacklistSite
from app.schemas.policy import BlacklistSiteResponse, BlacklistResponse
from app.api.dependencies import verify_agent

router = APIRouter()

@router.get("/policy/blacklist", response_model=BlacklistResponse, tags=["Policy"])
def get_blacklist(db: Session = Depends(get_db_mysql), agent = Depends(verify_agent)):
    sites = db.query(BlacklistSite).all()
    response_sites = [
        BlacklistSiteResponse(
            domain=site.domain,
            category=site.category,
            source=site.source,
            added_at=site.added_at
        ) for site in sites
    ]
    return {"sites": response_sites}
