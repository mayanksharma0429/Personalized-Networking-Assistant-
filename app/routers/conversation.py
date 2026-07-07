# app/routers/conversation.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models.db_models import UserProfile, EventContext, NetworkingSession, GeneratedStarter, WikipediaFactCheck
from app.models.schemas import (
    EventInput, 
    ConversationRequest, 
    FactCheckRequest, 
    ConversationResponse, 
    FactCheckResponse,
    FeedbackRequest
)

# Services
from app.services.event_analyzer import extract_event_themes
from app.services.topic_generator import generate_topics
from app.services.fact_checker import fact_check
from app.services.history_logger import log_conversation
from app.services.feedback_logger import log_feedback

router = APIRouter()

def get_or_create_dummy_session(db: Session):
    user = UserProfile(BioText="Anonymous")
    db.add(user)
    db.commit()
    event = EventContext(EventDescription="Unknown")
    db.add(event)
    db.commit()
    net_session = NetworkingSession(UserID=user.UserID, EventID=event.EventID)
    db.add(net_session)
    db.commit()
    return net_session.SessionID

@router.post("/analyze-event")
def analyze_event(data: EventInput, db: Session = Depends(get_db)):
    themes = extract_event_themes(data.description)
    return {"topics": themes}

@router.post("/fact-check", response_model=FactCheckResponse)
def fact_check_endpoint(data: FactCheckRequest, db: Session = Depends(get_db)):
    summary = fact_check(data.query)
    
    # Save to database
    session_id = get_or_create_dummy_session(db)
    fact_record = WikipediaFactCheck(
        SessionID=session_id,
        VerifiedQueryText=data.query,
        VerificationStatus="Checked",
        WikipediaSourceURL="https://en.wikipedia.org" if "error" not in summary.lower() else None
    )
    db.add(fact_record)
    db.commit()
    
    return FactCheckResponse(summary=summary)

@router.post("/generate-conversation", response_model=ConversationResponse)
def generate_conversation_endpoint(data: ConversationRequest, db: Session = Depends(get_db)):
    # Create DB context
    user = UserProfile(BioText=" | ".join(data.interests))
    db.add(user)
    db.commit()
    
    themes = extract_event_themes(data.description)
    
    event = EventContext(EventDescription=data.description, AnalyzedThemes=json.dumps(themes))
    db.add(event)
    db.commit()
    
    net_session = NetworkingSession(UserID=user.UserID, EventID=event.EventID)
    db.add(net_session)
    db.commit()
    
    # Generate topics
    suggestions = generate_topics(themes, data.interests)
    
    # Save generated starters to DB
    for starter in suggestions:
        db_starter = GeneratedStarter(
            SessionID=net_session.SessionID,
            StarterText=starter,
            ContextPromptUsed=data.description
        )
        db.add(db_starter)
    db.commit()
    
    # Log history
    history_data = {
        "event_description": data.description,
        "user_interests": data.interests,
        "extracted_themes": themes,
        "generated_suggestions": suggestions
    }
    log_conversation(history_data, db, net_session.SessionID)
    
    return ConversationResponse(topics=themes, suggestions=suggestions)

@router.post("/submit-feedback")
def submit_feedback_endpoint(data: FeedbackRequest, db: Session = Depends(get_db)):
    feedback_data = {
        "user_id": data.user_id,
        "rating": data.rating,
        "comments": data.comments
    }
    log_feedback(feedback_data, db)
    return {"message": "Feedback submitted successfully!"}
