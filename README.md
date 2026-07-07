# Personalized Networking Assistant

## Introduction
The Personalized Networking Assistant is an AI-powered web application designed to help professionals prepare for events. It analyzes event descriptions using Natural Language Processing (NLP) to extract themes, generates personalized conversation starters based on user interests, and provides a quick fact-checking tool using Wikipedia.

## Team Roles
- **Mayank:** Project Leader + Streamlit (Frontend & State Management)
- **Member 2:** FastAPI Backend (Architecture, Routing, Logging)
- **Member 3:** AI Models (DistilBERT for theme extraction & GPT-2 for generation)
- **Member 4:** Wikipedia API (Fact Checker Service)
- **Member 5:** Testing, Documentation & QA

---

## Member 5: Testing Philosophy and Documentation

### 1. Testing Philosophy and Framework Selection
We adopted a **Test-Driven** approach to ensure the reliability of our AI and API services. We selected **Pytest** as our primary testing framework because of its simplicity and powerful fixture support. For API route testing, we utilized FastAPI's **TestClient** (powered by `httpx`), which allows us to simulate HTTP requests without starting a live server.

### 2. Testing the Services
- **Event Analyzer Service:** Tested to ensure DistilBERT correctly outputs a list of strings (themes) and respects the maximum limit of 3 themes.
- **Topic Generator Service:** Tested to verify GPT-2 generates contextually relevant sentences without breaking the application logic.
- **Fact Checker Service:** Tested to handle timeouts and network errors gracefully using mock Wikipedia queries.

### 3. Testing API Routes with httpx TestClient
We created `tests/test_api.py` which includes tests for:
- `GET /` (Root Endpoint)
- Unauthorized access handling (Verifying the `access_token` middleware)
- `POST /analyze-event`
- `POST /fact-check`

### 4. Running Tests and Interpreting Results
To run the automated tests locally:
```bash
pytest tests/
```
A successful run will show green dots for passing tests. Any failures will output a traceback highlighting the bug.

### 5. Manual Testing and Verification
In addition to automated tests, manual testing was performed via the Streamlit UI:
1. Entered various event descriptions to verify state persistence.
2. Verified that the Wikipedia API properly handles misspelled words and returns a "Not Found" message gracefully.
3. Submitted user feedback and manually verified the creation and structure of `feedback.json`.

---

## Links (Documentation References)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [Wikipedia REST API](https://en.wikipedia.org/api/rest_v1/#/)

## Conclusion
The Personalized Networking Assistant successfully integrates modern backend frameworks (FastAPI) with state-of-the-art NLP models (Hugging Face) and an intuitive frontend (Streamlit). By dividing the architecture into distinct micro-services (Event Analyzer, Topic Generator, Fact Checker), the team achieved a scalable and maintainable codebase. The thorough testing and logging mechanisms ensure the application remains robust and user-friendly.
