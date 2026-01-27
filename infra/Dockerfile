# ================================
# BASE IMAGE
# ================================
FROM python:3.9-slim

# ================================
# WORKING DIRECTORY
# ================================
# FIX: set a clear working directory inside container
WORKDIR /app

# ================================
# SYSTEM DEPENDENCIES
# ================================
# FIX: libpq-dev required for psycopg (PostgreSQL driver)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ================================
# PYTHON DEPENDENCIES
# ================================
# FIX: copy only requirements first (better Docker cache)
COPY api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# ================================
# APPLICATION CODE
# ================================
# FIX: copy FastAPI app
COPY api /app/api

# ================================
# DATA + SCRIPTS (VERY IMPORTANT FIX)
# ================================
# FIX: earlier Docker image had NO CSV data
# FIX: earlier Docker image had NO ingest scripts
# This is why populations / loci were empty
COPY data /app/data
COPY scripts /app/scripts

# ================================
# EXPOSE PORT
# ================================
EXPOSE 8000

# ================================
# START FASTAPI
# ================================
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
