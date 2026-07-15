# Personalized Networking Assistant

## Introduction
The Personalized Networking Assistant is an AI-powered web application designed to help professionals prepare for events. It analyzes event descriptions using Natural Language Processing (NLP) to extract themes, generates personalized conversation starters based on user interests, and provides a quick fact-checking tool using Wikipedia.

## Getting Started & Running Locally

Follow these steps to run both the frontend and backend servers on your local machine.

### Prerequisites
Make sure you have Python 3.10+ installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/mayanksharma0429/Personalized-Networking-Assistant-.git
cd Personalized-Networking-Assistant-
```

### 2. Set Up a Virtual Environment
**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> [!TIP]
> **Windows Path Length Issue:** If you encounter `OSError: [WinError 206] The filename or extension is too long` while installing PyTorch on Windows, create your virtual environment in a directory with a shorter path (e.g. `C:\venv_pna`) instead of inside your deep workspace directory:
> ```powershell
> python -m venv C:\venv_pna
> C:\venv_pna\Scripts\activate
> ```

### 3. Install Dependencies
Once the virtual environment is activated, run:
```bash
pip install -r requirements.txt
```

### 4. Run the Backend (FastAPI)
Start the FastAPI server in a terminal window:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
The backend API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 5. Run the Frontend (Streamlit)
Start the Streamlit application in a separate terminal window:
```bash
streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 127.0.0.1
```
Open your browser and visit **[http://127.0.0.1:8501](http://127.0.0.1:8501)** to start using the assistant.

---

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
