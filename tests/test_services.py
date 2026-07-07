import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import json

from app.models.db_models import Base, LogEntry
from app.services.history_logger import log_conversation
from app.services.feedback_logger import log_feedback

# Setup in-memory SQLite for testing
engine = create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_log_conversation(db_session):
    data = {"test_key": "test_value"}
    log_conversation(data, db_session, session_id=None)
    
    # Verify
    logs = db_session.query(LogEntry).filter(LogEntry.ActionType == "Conversation Generated").all()
    assert len(logs) == 1
    assert json.loads(logs[0].PayloadJSON) == data

def test_log_feedback(db_session):
    data = {"rating": "5", "comments": "great"}
    log_feedback(data, db_session, session_id=None)
    
    # Verify
    logs = db_session.query(LogEntry).filter(LogEntry.ActionType == "User Feedback").all()
    assert len(logs) == 1
    assert json.loads(logs[0].PayloadJSON) == data
