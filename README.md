# LinkHunter-AI 🚀
### Autonomous Network Parsing & Job Intelligence Engine

LinkHunter-AI is a full-stack, decoupled data intelligence platform that transforms your LinkedIn professional network and automated job marketplace listings into an actionable, referral-ready outreach dashboard. The system targets high-ticket B2B consulting roles and warm-referral pathways through programmatic data mining, LLM-powered semantic matchmaking, and serverless pipeline automation.

---

## 🗺️ Implementation Status

| Phase | Status |
|-------|--------|
| **Phase 1** — Core Architecture & Setup | ✅ Complete |
| **Phase 2** — Data Ingestion & Pipelines | ✅ Complete |
| **Phase 3** — Frontend Application Layer | ✅ Complete |
| **Phase 4** — AI Matchmaking Core | ✅ Complete |
| **Phase 5** — CI/CD & Cloud Automation | ✅ Complete |

---

## 🏗️ System Architecture

```mermaid
graph TD
    classDef phase1 fill:#ffe3e3,stroke:#cc0000,stroke-width:2px;
    classDef phase2 fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px;
    classDef phase3 fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef phase4 fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef phase5 fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;

    subgraph Backend ["FastAPI Backend (Phase 1-2)"]
        MA["main.py<br/>Entry point + CORS"]:::phase1
        DB["database.py<br/>Session pool"]:::phase1
        LG["logger.py<br/>Rich logging"]:::phase1
        SC["schemas.py<br/>Pydantic validation"]:::phase1
        MG["Alembic<br/>Migrations"]:::phase1
        CP["csv_parser.py<br/>Connection CSV ingestion"]:::phase2
        JS["job_scraper.py<br/>RapidAPI / JSearch"]:::phase2
        EE["excel_exporter.py<br/>Excel output"]:::phase2
    end

    subgraph AI ["AI Intelligence Layer (Phase 4)"]
        AM["ai_matcher.py<br/>Match coordinator"]:::phase4
        AE["ai_engine.py<br/>LLM execution"]:::phase4
        AC["ai_client.py<br/>API client"]:::phase4
        AH["ai_cache_handler.py<br/>Cache management"]:::phase4
        AD["ai_drafter.py<br/>Message drafting"]:::phase4
    end

    subgraph Frontend ["Next.js Frontend (Phase 3)"]
        NP["pages<br/>Connections / Jobs / Matches"]:::phase3
        SH["shadcn/ui<br/>Component library"]:::phase3
        RT["@tanstack/react-table<br/>Data tables"]:::phase3
        RC["recharts<br/>Analytics"]:::phase3
    end

    subgraph CI_CD ["CI/CD Pipeline (Phase 5)"]
        CI["ci-pipeline.yml<br/>Lint + Build + Migrate"]:::phase5
        CD["cd-pipeline.yml<br/>Docker + Deploy"]:::phase5
        DK["Dockerfile<br/>Containerization"]:::phase5
    end

    CSV[(LinkedIn CSV)] --> CP
    API[(RapidAPI Jobs)] --> JS
    CP --> DB[(PostgreSQL)]
    JS --> EE[(target_jobs.xlsx)]
    DB --> AM
    EE --> AM
    AM --> AE
    AE --> AC
    AH --> AM
    AD --> AM
    DB --> NP
    EE --> NP
    CI --> CD
    CD --> DK
```

---

## 📁 Project Structure

```
LinkHunter-AI/
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── main.py                   # FastAPI entry point, CORS, error handling
│   │   ├── api/                      # REST API routers
│   │   │   ├── connections.py        # Connection CRUD endpoints
│   │   │   ├── jobs.py               # Job listing endpoints
│   │   │   └── matches.py            # AI matchmaking endpoints
│   │   ├── core/                     # Core infrastructure
│   │   │   ├── database.py           # SQLAlchemy session management
│   │   │   ├── schemas.py            # Pydantic validation schemas
│   │   │   ├── logger.py             # Rich console logging
│   │   │   └── ai_client.py          # LLM API client wrapper
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   │   ├── connection.py         # LinkedIn connection model
│   │   │   ├── job.py                # Job listing model
│   │   │   └── cache.py              # Match cache model
│   │   ├── services/                 # Business logic
│   │   │   ├── csv_parser.py         # CSV → database ingestion
│   │   │   ├── job_scraper.py        # RapidAPI job fetching
│   │   │   ├── excel_exporter.py     # Excel workbook output
│   │   │   ├── ai_matcher.py         # Matchmaking coordinator
│   │   │   ├── ai_engine.py          # LLM prompt execution
│   │   │   ├── ai_cache_handler.py   # Match result caching
│   │   │   ├── ai_drafter.py         # Referral message drafting
│   │   │   └── scheduler.py          # Automated cron jobs
│   │   └── routers/                  # Additional route handlers
│   ├── migrations/                   # Alembic database migrations
│   │   └── versions/                 # Migration scripts
│   ├── Dockerfile                    # Multi-stage container build
│   └── pyproject.toml                # Python project config
│
├── frontend/                         # Next.js frontend
│   ├── app/                          # Pages (Next.js App Router)
│   │   ├── connections/              # Connection management page
│   │   ├── jobs/                     # Job listings page
│   │   └── matches/                  # AI match results page
│   ├── components/                   # React components
│   │   ├── layout/                   # Header, sidebar
│   │   └── ui/                       # shadcn/ui primitives
│   └── lib/                          # Utilities
│       ├── api.ts                    # API client configuration
│       └── utils.ts                  # Helper functions
│
├── ci-pipeline.yml                   # Azure DevOps CI pipeline
├── cd-pipeline.yml                   # Azure DevOps CD pipeline
└── architecture.md                   # Detailed architecture spec
```

---

## ✨ Key Features

- **📥 Connection Ingestion** — Parse LinkedIn connection CSV exports into a normalized PostgreSQL schema with duplicate detection
- **🔍 Job Scraping** — Fetch live job listings via RapidAPI / JSearch API with structured output to Excel
- **🧠 AI Matchmaking** — Semantic LLM evaluation (Gemini Flash / OpenAI) to identify referral pathways between your network and open roles
- **💬 AI Message Drafting** — Generate personalized referral request messages for matched connections
- **⚡ Smart Caching** — Cache match results by payload hash to avoid redundant LLM calls
- **📊 Dashboard UI** — Full Next.js frontend with data tables, analytics charts, and dark mode
- **🔄 Automated Pipelines** — Background scheduler for periodic job scraping and match processing
- **🚀 CI/CD** — Azure DevOps pipelines with automated testing, Docker build, and deployment
- **🐳 Containerized** — Multi-stage Docker build for production deployment to Cloud Run / Azure Container Apps

---

## 🚀 Running the Project

### Prerequisites

- **Python 3.12+** with [uv](https://docs.astral.sh/uv/) installed
- **Node.js 20+** with npm
- **PostgreSQL** database (local or cloud via Supabase/Neon)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Configure environment
cp .env.example .env          # Edit with your DATABASE_URL, API keys, etc.

# Install Python dependencies
uv sync

# Run database migrations
uv run alembic upgrade head

# Seed test data (optional)
uv run python seed_test_data.py

# Start the API server (default: http://localhost:8000)
uv run fastapi dev
```

### Frontend Setup

```bash
# Navigate to frontend directory (separate terminal)
cd frontend

# Install Node dependencies
npm install

# Configure environment
cp .env.local.example .env.local   # Set NEXT_PUBLIC_API_URL

# Start the dev server (default: http://localhost:3000)
npm run dev
```

### API Endpoints

Once running, the backend exposes these REST endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/connections/` | List all connections |
| `POST` | `/connections/upload` | Upload connection CSV |
| `GET` | `/jobs/` | List all job listings |
| `POST` | `/jobs/scrape` | Trigger job scraping |
| `GET` | `/matches/` | Get AI match results |
| `POST` | `/matches/run` | Execute matchmaking |

---

## 🐳 Docker Deployment

```bash
# Build the Docker image
docker build -t linkhunter-backend ./backend

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host/db \
  -e RAPIDAPI_KEY=your_key \
  -e LLM_API_KEY=your_key \
  linkhunter-backend
```

---

## 🔄 CI/CD Pipelines

The project includes Azure DevOps YAML pipelines:

- **CI Pipeline** (`ci-pipeline.yml`): Runs on PRs and commits to `main`
  - Backend: Provisions PostgreSQL, installs dependencies, runs Alembic migrations, validates schema
  - Frontend: Installs Node packages, runs production build check

- **CD Pipeline** (`cd-pipeline.yml`): Triggered on successful CI completion
  - Builds Docker image and pushes to Azure Container Registry
  - Deploys to Azure Container Apps

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | FastAPI (Python) |
| **ORM** | SQLAlchemy 2.0 |
| **Migrations** | Alembic |
| **Validation** | Pydantic v2 |
| **Frontend** | Next.js 16 (App Router) |
| **UI Components** | shadcn/ui, Tailwind CSS 4 |
| **Data Tables** | @tanstack/react-table |
| **Charts** | Recharts |
| **Database** | PostgreSQL (Supabase / Neon) |
| **LLM** | Gemini Flash / OpenAI API |
| **Container** | Docker (multi-stage build) |
| **CI/CD** | Azure DevOps Pipelines |
| **Package Manager** | uv (Python), npm (Node) |

---

## 📄 License

MIT