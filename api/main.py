# 🔥 STEP 1: setup JSON logging FIRST (before FastAPI starts)
from api.logging_config import setup_logging
setup_logging()   # ✅ VERY IMPORTANT: must be before app = FastAPI()

# --------------------------------------------

from fastapi import FastAPI
from .routers import populations, loci, profiles, evidence, matches, auth
from api.routers.health import router as health_router
from prometheus_fastapi_instrumentator import Instrumentator

# --------------------------------------------

app = FastAPI(title="Privacy-Aware Forensic DNA API")

# --------------------------------------------
# register all routers
app.include_router(health_router)        # HEALTHCHECK
app.include_router(auth.router)          # LOGIN / JWT
app.include_router(populations.router)
app.include_router(loci.router)
app.include_router(profiles.router)
app.include_router(evidence.router)
app.include_router(matches.router)

# --------------------------------------------
# 🔥 Prometheus metrics endpoint (/metrics)
Instrumentator().instrument(app).expose(app)

# --------------------------------------------
@app.get("/")
def root():
    return {"ok": True, "service": "dna-api"}