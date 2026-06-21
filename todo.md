### Phase 1: Core Architecture & Local Storage Layer
**Objective:** Establish the development sandbox environment, construct the relational database structures, and configure secure environment controls.
- Initialize project directory structure using `uv init`.
- Create a protected configurations layer using an absolute `.env` runtime context pattern.
- Configure local development PostgreSQL access properties and map connection utilities into a modular `database.py` entry point.
- Establish structural migration control blocks via an `alembic init` workspace initialization sweep.

### Phase 2: Ingestion Engines & Data Normalization
**Objective:** Build out the physical ingestion bridges that safely pull text profiles and target job listings into isolated local storage structures.
- Implement a CSV batch parsing pipeline (`import_connections.py`) that extracts and normalizes native professional contact variables into a relational layout.
- Build a REST service utility client (`job_hunter.py`) that executes authenticated external job marketplace requests via RapidAPI.
- Integrate `Pandas` processing blocks that cleanly transform dynamic API payloads into localized, filterable Excel ledger grids (`target_jobs.xlsx`).

### Phase 3: The AI Intelligence & Matchmaking Layer
**Objective:** Layer semantic AI processing onto the data architectures to automatically evaluate connection profiles against available roles.
- Build a cross-table analysis engine that reads structural entries from the database while parsing the external active Excel ledger blocks simultaneously.
- Create an extraction prompt template using structured context injections (System Roles, Few-Shot examples).
- Connect the script engine to an LLM runtime connection (via Gemini Flash or OpenAI API) to evaluate text parameters for specific context signals:
  - *Signal A:* Does connection X work at company Y which currently has an opening?
  - *Signal B:* Does connection Z have an engineering managerial title relevant to a specific role?
- Append an enriched `Internal Referrals Available` tracking data index column directly onto the final output sheets.

### Phase 4: CI/CD, Serverless Deployment, and Optimization
**Objective:** Move execution off your local development computer and automate the tracking pipelines inside the cloud for zero maintenance cost.
- Migrate your production schema state out to a serverless **Supabase** or **Neon** database node using `alembic upgrade head`.
- Containerize the executable Python orchestration logic by wrapping all dependency definitions inside a multi-stage `Dockerfile`.
- Deploy the lightweight container images straight into **Google Cloud Run** or **AWS Lambda**.
- Configure a **Cloud Scheduler** or **EventBridge** cron statement block to run the pipeline automatically on a recurring schedule (e.g., every morning at 8:00 AM).

---

## 4. Master Progress Tracking Dashboard

# Project Task Matrix: LinkHunter-AI Execution Dashboard

Use this tracking index sheet to manage progress blocks, feature iterations, and deployment validation cycles.

---

## 🟩 Phase 1: Core Architecture & Setup
- [x] Initialize local development workspace structure using `uv init`.
- [x] Configure a protected configurations layer using an absolute `.env` schema pattern.
- [x] Build connection routing parameter maps inside `database.py`.
- [x] Initialize system schema tracking states using `alembic init migrations`.
- [ ] Configure `migrations/env.py` to dynamically load parameters straight from `.env`.

---

## 🟦 Phase 2: Ingestion Engines & Data Normalization
- [ ] Implement database initialization table mappings inside a baseline `setup.py` module script.
- [ ] Write schema generation structures for `linkedin_connections` with explicit `UNIQUE` index keys.
- [ ] Write the CSV batch scanning loop parser inside `import_connections.py` to handle structural contact imports cleanly.
- [ ] Setup account tokens on RapidAPI and test live API query connectivity to the JSearch engine using `requests`.
- [ ] Build the core wrapper loop inside `job_hunter.py` to strip JSON data arrays.
- [ ] Integrate `Pandas` and `OpenPyXL` to format and output structured arrays into `target_jobs.xlsx`.

---

## 🟪 Phase 3: Frontend Application Layer
- [ ] Bootstrap the web interface app directory using `npx create-next-app@latest --typescript --tailwind`.
- [ ] Run initialization configurations for the component kit: `npx shadcn-ui@latest init`.
- [ ] Build a robust layout system featuring consistent Sidebar components, typography foundations, and Dark Mode default overrides.
- [ ] Install table engines (`npm i @tanstack/react-table`) and build a dashboard view page mapping the active connections data table grid.
- [ ] Build a custom Job Board view panel implementing card templates that highlight the enriched `Internal Referrals Available` tags.
- [ ] Install visualization tools (`npm i tremor`) and display data metrics tracking company densities and application status logs.

---

## 🟨 Phase 4: AI Intelligence & Matchmaking
- [ ] Build the query execution block inside `matcher.py` that loads relational rows and spreadsheet data simultaneously.
- [ ] Design a structured system instruction prompt matrix utilizing a rigid context layout format.
- [ ] Integrate the API client tracking modules to securely forward context strings to the LLM execution pipeline.
- [ ] Write custom parsing functions to capture the structured text payloads returned from the LLM.
- [ ] Implement the file appending operations to write final matched candidate reports back into the spreadsheet rows.

---

## 🚀 Phase 5: Cloud Infrastructure & Automation
- [ ] Spin up a free production database container instance on Supabase or Neon.
- [ ] Re-route local environment target definitions onto the new production cloud URI string parameters.
- [ ] Execute `alembic upgrade head` inside the terminal window to build structures in the cloud.
- [ ] Author a production-ready multi-stage `Dockerfile` to optimize image compilation footprints.
- [ ] Deploy the micro-container infrastructure layers straight to Google Cloud Run / AWS Lambda.
- [ ] Configure a Cloud Scheduler / EventBridge chron task timer rule to automatically trigger processing sweeps daily.