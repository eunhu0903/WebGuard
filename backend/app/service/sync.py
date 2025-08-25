from sqlalchemy.orm import Session
from app.db.models import BlacklistSite
from app.db.session import get_db_mysql, get_db_pg

def sync_blacklist(mysql_db: Session, pg_db: Session):
    mysql_sites = mysql_db.query(BlacklistSite).all()
    synced_count = 0

    for site in mysql_sites:
        exists = pg_db.query(BlacklistSite).filter_by(domain=site.domain).first()
        if not exists:
            new_site = BlacklistSite(
                domain=site.domain,
                category=site.category,
                source=site.source,
                added_at=site.added_at
            )
            pg_db.add(new_site)
            synced_count += 1
        
    if synced_count:
        pg_db.commit()
    
    return synced_count