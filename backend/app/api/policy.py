from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import BlacklistSite
from app.schemas.policy import BlacklistSiteResponse, BlacklistResponse
from app.api.dependencies import verify_agent

router = APIRouter()

@router.get("/policy/blacklist", response_model=BlacklistResponse)
def get_blacklist(db: Session = Depends(get_db)):
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
