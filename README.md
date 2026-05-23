# Closira Backend Service

Professional, production-aware FastAPI backend for an AI-powered customer communication platform. This service handles enquiry intake, automated SOP matching, follow-ups, and escalation workflows with a full CRM-style audit trail.

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
├── services/       # Business logic (SOP, History, Follow-up, Escalation)
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

The project maintains a comprehensive test suite (currently 25/25 passing):
```bash
python -m pytest
```

## 🧠 Architecture Decisions

- **Acknowledgement Pattern**: `POST /enquiry` returns a tracking ID and `queued` state immediately. This reflects a real-world async CRM ingestion pipeline.
- **SOP Matching Engine**: A deterministic keyword-driven service in `app/services/sop_matcher.py`. Designed to be easily swapped with an LLM/AI model in the future.
- **CRM Timeline (History)**: Every enquiry lifecycle change is recorded as a `HistoryEvent` with JSON metadata for full auditability.
- **Idempotent Escalations**: The escalation endpoint ensures that multiple triggers for the same management review state do not result in duplicate audit logs or state inconsistency.
- **Service Isolation**: Route handlers are thin; all business logic resides in specialized services (Enquiry, Followup, Escalation, History).
- **Date Handling**: Centralized UTC handling in `app/utils/time.py` to ensure consistency across services and the database.

## 📡 Key Endpoints

### Enquiry Management

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/enquiry/` | Intake a new customer enquiry (Async). |
| `GET` | `/enquiry/{id}/history` | Fetch the full CRM activity timeline for an enquiry. |
| `POST` | `/enquiry/{id}/follow-up` | Schedule an automated follow-up message. |
| `POST` | `/enquiry/{id}/escalate` | Manually escalate toward management review. |

### System
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Enhanced health check with database connectivity report. |

## 📈 Current Progress

- [x] **Foundation**: Structured logging, Global Exceptions, Health Monitoring.
- [x] **Domain Core**: SQLAlchemy 2.0 Models, Pydantic v2 schemas.
- [x] **Enquiry Intake**: REST endpoint with BackgroundTask integration.
- [x] **Auto-Processor**: Keyword-based SOP matching engine.
- [x] **Audit Trail**: History service for transparent activity logging.
- [x] **Follow-up Flow**: Delay-based message scheduling logic.
- [x] **Escalation Hub**: Idempotent priority management.
- [x] **Timeline View**: Chronological history aggregation and display.
