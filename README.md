# 🧬 Forensic DNA Analysis – FastAPI + DevOps Project

This is a Dockerized FastAPI backend for a Privacy-Aware Forensic DNA Analysis System using PostgreSQL.  
The project demonstrates backend development with DevOps practices such as Docker, Docker Compose, environment variables, and data ingestion pipelines.

---

## 🚀 Tech Stack

- FastAPI (Python)
- PostgreSQL
- JWT Authentication (RBAC)
- Docker & Docker Compose

---

## 📁 Project Structure

```text
forensic-dna-fastapi-devops/
├── api/            # FastAPI application
├── infra/          # Docker & infrastructure (Dockerfile, docker-compose, SQL init)
├── scripts/        # Data ingestion scripts
├── data/           # CSV / Excel datasets
└── README.md


⸻

⚙️ How to Run (Mac / Windows / Linux)

git clone https://github.com/sangam1814/forensic-dna-fastapi-devops.git
cd forensic-dna-fastapi-devops/infra
docker-compose up --build

After startup:
	•	API: http://localhost:8000
	•	Docs (Swagger UI): http://localhost:8000/docs

⸻

🔐 Authentication

POST /auth/login

{
  "email": "admin",
  "password": "admin"
}

Returns a JWT token for authorized access.

⚠️ Default credentials are for demo purposes only.

⸻

📊 Data Ingestion

Run inside Docker to load DNA data:

docker-compose run api python /app/scripts/ingest_profiles.py

This loads:
	•	Populations
	•	STR loci
	•	DNA profiles
	•	Genotype data

⸻

🧪 Example APIs
	•	GET /populations
	•	GET /loci
	•	GET /profiles/{sample_id}

⸻

🛠 DevOps Highlights
	•	Dockerized FastAPI backend
	•	PostgreSQL container with initialization scripts
	•	Environment variables for DB and security config
	•	Data ingestion via Docker-executed scripts
	•	One-command startup using Docker Compose

⸻

👤 Author

Sangam Raj
GitHub: https://github.com/sangam1814
