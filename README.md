---

# 🧬 Forensic DNA Analysis – FastAPI + DevOps Project

This project is a **Dockerized FastAPI backend** for a Privacy-Aware Forensic DNA Analysis System using **PostgreSQL**.
It demonstrates backend development combined with **DevOps practices** such as containerization, service orchestration, monitoring, and centralized logging.

---

## 🚀 Tech Stack

* Python (FastAPI)
* PostgreSQL
* JWT Authentication (Admin-only)
* Docker & Docker Compose
* Prometheus (Monitoring)
* Grafana (Metrics Visualization)
* Promtail & Loki (Centralized Logging)

---

## 📁 Project Structure

```text
forensic-dna-fastapi-devops/
├── api/                 # FastAPI application
│   ├── main.py
│   ├── logging_config.py
│   └── routers/
├── infra/               # Infrastructure and DevOps configs
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── prometheus.yml
│   └── promtail.yml
├── scripts/             # Data ingestion scripts
├── data/                # CSV datasets
└── README.md
```

---

## ⚙️ How to Run the Project (Mac / Linux / Windows)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/sangam1814/forensic-dna-fastapi-devops.git
```

### 2️⃣ Navigate to infrastructure directory

```bash
cd forensic-dna-fastapi-devops/infra
```

### 3️⃣ Build and start all services

```bash
docker-compose up --build
```

✅ This starts all services, but **the database will be empty initially**.

---

## 📊 Data Ingestion (REQUIRED)

⚠️ **This step is mandatory. APIs will not return data until ingestion is completed.**

Open a **new terminal window**, then run:

```bash
cd forensic-dna-fastapi-devops/infra
docker-compose run api python /app/scripts/ingest_profiles.py
```

This command loads:

* Populations
* Loci
* DNA profiles
* Genotypes

into the PostgreSQL database.

---

## 🌐 Service URLs

* **API**: [http://localhost:8000](http://localhost:8000)
* **Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Prometheus**: [http://localhost:9090](http://localhost:9090)
* **Grafana**: [http://localhost:3000](http://localhost:3000)

  * Default credentials: `admin / admin`

---

## 🔐 Authentication (Admin Only)

**POST** `/auth/login`

```json
{
  "email": "admin",
  "password": "admin"
}
```

Returns a **JWT token** required for accessing protected APIs.

---

## 🧪 Example API Endpoints

* **GET** `/populations`
* **GET** `/loci`
* **GET** `/profiles/{sample_id}`

(Requires JWT token)

---

## 📈 Monitoring & Logging

* **Prometheus** collects application and system metrics.
* **Grafana** visualizes metrics using dashboards.
* **Promtail** collects container logs.
* **Loki** stores and enables querying of logs.
* Application logs are written in a structured format to support observability and debugging.

---

## 🛠 DevOps Highlights

* Containerized backend and database services using Docker
* Managed multi-service setup using Docker Compose
* Integrated monitoring for application and system health
* Implemented centralized logging for containers and application logs
* Used environment variables for runtime configuration
* Enabled full stack startup using simple Docker Compose commands

---

## 👤 Author

**Sangam Raj**
GitHub: [https://github.com/sangam1814](https://github.com/sangam1814)

---
