from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base

# Dynamic initialization of schema blueprints
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LinkHunter-AI Backend Gateway",
    version="1.0.0",
    description="Scalable automation data infrastructure & semantic evaluation engine."
)

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
    return {"status": "operational", "engine": "LinkHunter-AI Framework Core"}