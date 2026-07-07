import json
from sqlalchemy.orm import Session
from app.models.db_models import LogEntry

def log_feedback(data: dict, db: Session, session_id: int = None):
    """
    Saves user feedback to the LogEntry table in the database.
    """
    log_entry = LogEntry(
        SessionID=session_id,
        ActionType="User Feedback",
        PayloadJSON=json.dumps(data)
    )
    db.add(log_entry)
    db.commit()
