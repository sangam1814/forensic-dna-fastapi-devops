# 🧬 Forensic DNA Analysis – FastAPI + DevOps Project

This is a Dockerized FastAPI backend for a Privacy-Aware Forensic DNA Analysis System using PostgreSQL.  
The project demonstrates backend development with DevOps practices like Docker, docker-compose, environment variables, and data ingestion pipelines.

---

## 🚀 Tech Stack

- FastAPI (Python)
- PostgreSQL
- JWT Authentication (RBAC)
- Docker & Docker Compose

---

## 📁 Project Structure

```text
forensic_dna_backend/
├── api/            # FastAPI application
├── infra/          # Docker & infrastructure (Dockerfile, docker-compose, SQL init)
├── scripts/        # Data ingestion scripts
├── data/           # CSV / Excel datasets
└── README.md
```

---

## ⚙️ How to Run (Mac/Windows/Linux)

```bash
git clone https://github.com/sangam1814/forensic-dna-fastapi-devops.git
Note: Open the terminal inside the cloned project folder (or navigate to it using the correct path).
cd forensic-dna-fastapi-devops/infra
docker-compose up --build

	•	API: http://localhost:8000
	•	Docs: http://localhost:8000/docs

⸻

🔐 Authentication

POST /auth/login

{
  "email": "admin",
  "password": "admin"
}

Returns JWT token for authorized access.

⸻

📊 Data Ingestion

Run inside Docker:

open new terminal terminal.

go to infra folder.

then execute the cmd below.

docker-compose run api python /app/scripts/ingest_profiles.py

Loads populations, loci, profiles, and genotypes into the database.

⸻

🧪 Example APIs
	•	GET /populations
	•	GET /loci
	•	GET /profiles/{sample_id}

⸻

🛠 DevOps Highlights
	•	Dockerized FastAPI service
	•	PostgreSQL container
	•	DB initialization using SQL scripts
	•	Environment variables for configuration
	•	One-command startup

⸻

👤 Author

Sangam Raj
GitHub: https://github.com/sangam1814
