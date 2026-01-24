from fastapi import FastAPI
from .routers import populations, loci, profiles, evidence, matches, auth
from api.routers.health import router as health_router

app = FastAPI(title="Privacy-Aware Forensic DNA API")

# register all routers
app.include_router(health_router)        # HEALTHCHECK
app.include_router(auth.router)           # LOGIN / JWT
app.include_router(populations.router)
app.include_router(loci.router)
app.include_router(profiles.router)
app.include_router(evidence.router)
app.include_router(matches.router)

@app.get("/")
def root():
    return {"ok": True, "service": "dna-api"}