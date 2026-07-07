# app/services/event_analyzer.py

from transformers import pipeline
from app.config import MODEL_NAMES

# Module-level instantiation taaki model ek hi baar start mein load ho (fast processing)
classifier = pipeline("zero-shot-classification", model=MODEL_NAMES["event_analysis"])

def extract_event_themes(description: str, candidate_labels=None):
    # Default labels agar koi list provide na ki jaye
    if candidate_labels is None:
        candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability", "business", "technology"]
    
    # Model se classification karwana
    result = classifier(description, candidate_labels)
    
    # Sirf top 3 highest-scoring themes return karna
    return result["labels"][:3]
