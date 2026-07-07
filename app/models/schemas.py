# app/models/schemas.py

from pydantic import BaseModel
from typing import List

# 1. Event Input Model
class EventInput(BaseModel):
    description: str

# 2. User Interests Model
class UserInterests(BaseModel):
    interests: List[str]

# 3. Conversation Request Model
class ConversationRequest(BaseModel):
    description: str
    interests: List[str]

# 4. Conversation Response Model
class ConversationResponse(BaseModel):
    topics: List[str]
    suggestions: List[str]

# 5. Fact Check Request Model
class FactCheckRequest(BaseModel):
    query: str

# 6. Fact Check Response Model
class FactCheckResponse(BaseModel):
    summary: str
    
# 7. Feedback Request Model
class FeedbackRequest(BaseModel):
    user_id: str = "anonymous"
    rating: str
    comments: str
