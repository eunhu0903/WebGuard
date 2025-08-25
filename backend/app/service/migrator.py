from app.db.session import SessionLocalMySQL, SessionLocalPG
from app.db.models import UserLog

def migrate_logs(batch_size: int = 1000):
    pg_db = SessionLocalPG()
    my_db = SessionLocalMySQL()

    try:
        logs = pg_db.query(UserLog).limit(batch_size).all()
        if not logs:
            return "옮길 로그 없음"
        
        for log in logs:
            my_db.merge(log)
            pg_db.delete(log)
        
        my_db.commit()
        pg_db.commit()
        return f"{len(logs)}개 로그 MySQL로 이동 완료"
    except Exception as e:
        pg_db.rollback()
        my_db.rollback()
        raise e
    finally:
        pg_db.close()
        my_db.close()