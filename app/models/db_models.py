from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profile"
    
    UserID = Column(Integer, primary_key=True, index=True)
    BioText = Column(Text, nullable=True)
    CurrentEventCache = Column(Text, nullable=True)
    
    sessions = relationship("NetworkingSession", back_populates="user")

class EventContext(Base):
    __tablename__ = "event_context"
    
    EventID = Column(Integer, primary_key=True, index=True)
    EventDescription = Column(Text, nullable=False)
    AnalyzedThemes = Column(Text, nullable=True)
    
    sessions = relationship("NetworkingSession", back_populates="event")

class NetworkingSession(Base):
    __tablename__ = "networking_session"
    
    SessionID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("user_profile.UserID"), nullable=False)
    EventID = Column(Integer, ForeignKey("event_context.EventID"), nullable=False)
    SessionTimestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("UserProfile", back_populates="sessions")
    event = relationship("EventContext", back_populates="sessions")
    starters = relationship("GeneratedStarter", back_populates="session")
    fact_checks = relationship("WikipediaFactCheck", back_populates="session")
    logs = relationship("LogEntry", back_populates="session")

class GeneratedStarter(Base):
    __tablename__ = "generated_starter"
    
    StarterID = Column(Integer, primary_key=True, index=True)
    SessionID = Column(Integer, ForeignKey("networking_session.SessionID"), nullable=False)
    StarterText = Column(Text, nullable=False)
    ContextPromptUsed = Column(Text, nullable=True)
    
    session = relationship("NetworkingSession", back_populates="starters")

class WikipediaFactCheck(Base):
    __tablename__ = "wikipedia_fact_check"
    
    FactCheckID = Column(Integer, primary_key=True, index=True)
    SessionID = Column(Integer, ForeignKey("networking_session.SessionID"), nullable=False)
    VerifiedQueryText = Column(Text, nullable=False)
    VerificationStatus = Column(String(50), nullable=False)
    WikipediaSourceURL = Column(String(255), nullable=True)
    
    session = relationship("NetworkingSession", back_populates="fact_checks")

class LogEntry(Base):
    __tablename__ = "log_entry"
    
    LogID = Column(Integer, primary_key=True, index=True)
    SessionID = Column(Integer, ForeignKey("networking_session.SessionID"), nullable=True)
    ActionType = Column(String(100), nullable=False)
    PayloadJSON = Column(Text, nullable=True)
    Timestamp = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("NetworkingSession", back_populates="logs")
