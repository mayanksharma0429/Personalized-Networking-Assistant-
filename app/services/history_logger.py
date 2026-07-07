import json
from sqlalchemy.orm import Session
from app.models.db_models import LogEntry, NetworkingSession

def log_conversation(data: dict, db: Session, session_id: int = None):
    """
    Saves conversation history to the LogEntry table in the database.
    """
    log_entry = LogEntry(
        SessionID=session_id,
        ActionType="Conversation Generated",
        PayloadJSON=json.dumps(data)
    )
    db.add(log_entry)
    db.commit()
