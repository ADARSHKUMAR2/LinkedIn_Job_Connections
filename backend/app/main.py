from app.core.logger import log
from rich.traceback import install
install(show_locals=True)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from rich.console import Console
console = Console()
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models.connection import LinkedInConnection
from app.models.job import JobListing
from app.api.matches import router as matches_router
from app.api.connections import router as connections_router  
from app.api.jobs import router as jobs_router
from app.services.scheduler import start_automated_cron_jobs, shutdown_automated_cron_jobs
from contextlib import asynccontextmanager

# Dynamic initialization of schema blueprints
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Startup Phase: Boot the background worker loop
    start_automated_cron_jobs()
    yield
    # 🛑 Teardown Phase: Safely close worker execution threads
    shutdown_automated_cron_jobs()

app = FastAPI(
    title="LinkHunter-AI Backend Gateway",
    version="1.0.0",
    description="Scalable automation data infrastructure & semantic evaluation engine.",
    lifespan=lifespan
)

app.include_router(matches_router)
app.include_router(connections_router)
app.include_router(jobs_router)

# Enable immediate cross-origin integration handles for Phase 3 (Next.js client)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tighten down in production deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root_health_check():
    log.info("🚀 [bold green]FastAPI Server is starting up![/bold green]")
    return {"status": "online", "engine": "LinkHunter-AI Framework Core"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # This forces rich to print the error with the exact line highlighted
    console.print_exception(show_locals=True)
    
    # Return a standard 500 error to the user/client
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )