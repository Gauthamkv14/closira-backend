# Closira Backend Service

Professional, production-aware FastAPI backend for an AI-powered customer communication platform. This service handles enquiry intake, automated SOP matching, follow-ups, and escalation workflows.

## 🚀 Tech Stack

- **Core**: FastAPI (Python 3.10+)
- **Database**: SQLite with SQLAlchemy 2.0 ORM
- **Validation**: Pydantic v2
- **Logging**: Structured JSON Logging
- **Scheduling**: FastAPI BackgroundTasks (Async simulation)
- **Formatting**: Ruff + Black
- **Testing**: Pytest with in-memory SQLite

## 📂 Folder Structure

```text
backend/
├── app/
│   ├── api/            # API routes and dependencies
│   ├── core/           # Config, logging, enums, exceptions
│   ├── db/             # Models and session management
│   ├── schemas/        # Pydantic validation models
│   ├── services/       # Business logic layer
│   ├── workers/        # Background task processing
│   └── utils/          # Utility helpers
├── tests/              # Pytest suite
├── docs/               # Architecture and decision logs
└── requirements.txt    # Dependency list
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
   Copy `.env.example` to `.env` and adjust as needed.

## 🏃 Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```
The API documentation will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧪 Running Tests

```bash
python -m pytest
```

## 🧠 Architecture Decisions

- **Domain-Driven Models**: Intentional CRM-like modeling for enquiries, history, and follow-ups.
- **Service Layer**: Business logic is decoupled from API routes to maintain "Clean Architecture" principles.
- **Structured Logging**: JSON format logs ensure observability in production environments.
- **SQLite for Assignment**: Zero-latency local setup while maintaining ACID compliance via SQLAlchemy.
- **BackgroundTasks**: Used to simulate async AI processing (SOP matching) without the overhead of Celery/Redis.

## 📈 Current Progress

- [x] Foundation (Logger, Database, Exceptions)
- [x] Domain Modeling & Validation
- [x] API Refinement & Documentation
- [ ] Service Layer (In-progress)
- [ ] Background Worker (Pending)
- [ ] Integration Testing (Pending)
