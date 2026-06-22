# LinkHunter-AI 🚀
### Autonomous Network Parsing & Job Intelligence Engine

LinkHunter-AI is a full-stack, decoupled data intelligence application designed to convert your professional network records and automated public job marketplace listings into an actionable, referral-ready outreach dashboard. 

By bypassing the traditional corporate recruitment funnel, the system targets high-ticket B2B consulting roles and warm-referral warm paths through programmatic data mining, serverless data pipeline execution, and semantic LLM matchmaking.

---

## 🗺️ System Implementation Roadmap

- **[PHASE 1]** Core Architecture & Setup
  -  └── *Next Step* ➔ **[PHASE 2]** Data Ingestion & Pipelines
      -  └── *Next Step* ➔ **[PHASE 3]** Frontend Application Layer
          -  └── *Next Step* ➔ **[PHASE 4]** AI Matchmaking Core
              -  └── *Final Step* ➔ **[PHASE 5]** CI/CD & Cloud Automation

---

## 🏗️ System Architecture

```mermaid
graph TD
    %% Define Style Classes for High Visual Scannability
    classDef phase1 fill:#ffe3e3,stroke:#cc0000,stroke-width:2px;
    classDef phase2 fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px;
    classDef phase3 fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef phase4 fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef phase5 fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    classDef storage fill:#fffde7,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5;

    %% Storage Layer Component Nodes
    subgraph Storage [Storage & Artifact Matrices]
        CSV[LinkedIn Connection CSV]:::storage
        API_Data[RapidAPI / JSearch Feed]:::storage
        Postgres[(PostgreSQL Cloud: Supabase/Neon)]:::storage
        Excel[target_jobs.xlsx Workbook]:::storage
    end

    %% Phase 1
    subgraph P1 [Phase 1: Core Architecture & Local Storage Layer]
        UV[uv Python Workspace]
        Env[.env Secrets Core]
        DB_Py[database.py Session Pool]
        Alembic[Alembic Migrations / env.py]
    end
    class P1 phase1;

    %% Phase 2
    subgraph P2 [Phase 2: Ingestion Engines & Data Normalization]
        Setup[setup.py Initialization]
        Schema[linkedin_connections Schema]
        ImportConn[import_connections.py]
        JobHunter[job_hunter.py Client]
        PandasEngine[Pandas + OpenPyXL Engine]
    end
    class P2 phase2;

    %% Phase 3
    subgraph P3 [Phase 3: Frontend Application Layer]
        NextApp[Next.js App: TS + Tailwind]
        Shadcn[shadcn-ui Components]
        ReactTable["@tanstack/react-table Display"]
        TremorUI[Tremor Analytics Engine]
    end
    class P3 phase3;

    %% Phase 4
    subgraph P4 [Phase 4: AI Intelligence & Matchmaking Layer]
        Matcher[matcher.py Coordinator]
        Prompt[Structured Prompt Template]
        LLM[LLM API: Gemini Flash / OpenAI]
    end
    class P4 phase4;

    %% Phase 5
    subgraph P5 [Phase 5: CI/CD, Serverless Deployment, & Optimization]
        Docker[Dockerfile: Multi-stage Build]
        Serverless[Google Cloud Run / AWS Lambda]
        Cron[Cloud Scheduler / EventBridge]
    end
    class P5 phase5;

    %% Operational Pipelines & Control Flows
    UV --> P1
    Env -->|Exposes Variables| DB_Py
    Env -->|Hydrates| Alembic
    Setup -->|Builds Constraints| Schema
    Schema -->|Executes Against| Postgres
    Alembic -->|Pushes Structural Migrations| Postgres
    CSV -->|Read & Tokenized By| ImportConn
    ImportConn -->|Bulk Ingestion Loop| Postgres
    API_Data -->|Programmatic REST Sucking| JobHunter
    Env -->|Injects RAPIDAPI_KEY| JobHunter
    JobHunter -->|Clean JSON Arrays| PandasEngine
    PandasEngine -->|Saves Structured File| Excel
    Postgres -->|Queries Unique Connection Rows| Matcher
    Excel -->|Parses Open Job Target Listings| Matcher
    Prompt -->|Contextual Instructions| Matcher
    Matcher <-->|Semantic Matching Loops| LLM
    Matcher -->|Writes Back Internal Referrals Field| Excel
    Postgres -->|Hydrates Connection Grids| ReactTable
    Excel -->|Hydrates Aggregated Open Jobs| ReactTable
    ReactTable -->|Renders Client Side Filters| NextApp
    TremorUI -->|Visualizes Company Densities & Pipelines| NextApp
    Shadcn -->|Composes Theme & Shell System| NextApp
    Docker -->|Compiles Deployment Artifact Bundle| Serverless
    Cron -->|Daily Cron Heartbeat Trigger 08:00 AM| Serverless
    Serverless -->|Automates Pipeline Job Hunting Run| JobHunter
    Serverless -->|Automates Data Cross Match Processing| Matcher

```


