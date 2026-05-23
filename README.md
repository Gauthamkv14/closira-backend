# Closira Backend Service

Professional, production-aware FastAPI backend for an AI-powered customer communication platform. This service handles enquiry intake, automated SOP matching, follow-ups, and escalation workflows.

## 🚀 Tech Stack

- **Core**: FastAPI (Python 3.13+)
- **Database**: SQLite with SQLAlchemy 2.0 ORM
- **Validation**: Pydantic v2
- **Logging**: Structured JSON Logging (python-json-logger)
- **Scheduling**: FastAPI BackgroundTasks (Async processing simulation)
- **Tooling**: Ruff (Linter) + Black (Formatter)
- **Testing**: Pytest with in-memory SQLite and shared connection pool

## 📂 Folder Structure

```text
app/
├── api/            # Routes (Enquiries, Health) and Dependencies
├── core/           # Config, logging, enums, centralized exceptions
├── db/             # SQLAlchemy Models and Session management
├── schemas/        # Pydantic validation & response models
├── services/       # Business logic (SOP Matcher, Enquiry Service)
├── workers/        # Async background task processors
└── utils/          # Time utilities and helpers
tests/              # Comprehensive test suite (Unit, Integration, Worker)
```

## 🛠️ Setup Instructions

1. **Clone the repository**
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate     # Unix/macOS
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Configuration**:
   The app uses `.env` for configuration. Copy `.env.example` to `.env`.

## 🏃 Running the Application

```bash
uvicorn app.main:app --reload
```
Review the interactive API docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧪 Running Tests

The project maintains a strict testing threshold (currently 16/16 passing):
```bash
python -m pytest
```

## 🧠 Architecture Decisions

- **Acknowledgement Pattern**: `POST /enquiry` returns a tracking ID and `queued` state immediately. This reflects a real-world async CRM ingestion pipeline.
- **SOP Matching Engine**: A deterministic keyword-driven service in `app/services/sop_matcher.py`. Designed to be easily swapped with an LLM/AI model in the future.
- **CRM Timeline (History)**: Every enquiry lifecycle change (creation, SOP match, escalation) is recorded as a `HistoryEvent` with JSON metadata for auditability.
- **Service Isolation**: Route handlers are kept thin; all database transactions and complex logic reside in the `Service` layer.
- **SQLite Concurrency**: Configured with `StaticPool` and `check_same_thread=False` to handle FastAPI's multi-threaded worker dispatch safely.

## 📡 Key Endpoints

### Health Check
`GET /health`
- **Response**: `{"status": "healthy", "database": "connected", "timestamp": "..."}`

### Enquiry Intake
`POST /enquiry/`
- **Purpose**: High-speed induction of customer messages.
- **Payload**:
  ```json
  {
    "customer_name": "Sarah Johnson",
    "channel": "email",
    "message": "Can you share your pricing plans?"
  }
  ```
- **Response (Immediate Acknowledgement)**:
  ```json
  {
    "enquiry_id": 1,
    "status": "received",
    "processing_state": "queued",
    "created_at": "2026-05-23T16:17:42Z"
  }
  ```

## 📈 Current Progress

- [x] **Foundation**: Structured logging, Global Exceptions, Health Monitoring.
- [x] **Domain Core**: SQLAlchemy 2.0 Models, Pydantic v2 schemas.
- [x] **Enquiry Intake**: REST endpoint with BackgroundTask integration.
- [x] **Auto-Processor**: Keyword-based SOP matching engine.
- [x] **Audit Trail**: History event persistence for every state change.
- [ ] **Follow-up Flow**: Scheduled messaging system (Next).
- [ ] **Escalation Hub**: Specialized endpoints for management review.
- [ ] **Timeline View**: History fetching and aggregation.
