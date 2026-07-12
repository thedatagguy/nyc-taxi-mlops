# NYC Taxi Trip Duration — Production ML Pipeline

An end-to-end MLOps project that simulates a real production ML system:
NYC TLC publishes trip data monthly → this pipeline ingests each new
month, validates the schema, checks for data drift, conditionally
retrains, and serves the current production model via an API.

## Problem Statement
Predict taxi trip duration from pickup-time features (location zones,
time of day, day of week, trip distance). The prediction task is
deliberately simple — the focus of this project is the **operational
lifecycle around the model**, not model complexity.

## Why this dataset
- Monthly release cadence → natural retraining trigger (real production
  loop, not a simulated one)
- Millions of rows/month → PySpark is justified, not decorative
- Known schema variations across months → real schema-drift handling
- Seasonal/temporal patterns → drift detection has something to detect

## Architecture
[diagram placeholder — add after Phase 1]

Ingestion → Schema Validation → PySpark Processing → Training (MLflow)
→ Drift Check (Evidently) → Conditional Retrain → Registry Promotion
→ FastAPI Serving → Monitoring

## Tech Stack
| Concern | Tool |
|---|---|
| Data versioning | DVC |
| Processing | PySpark |
| Experiment tracking & registry | MLflow |
| Drift detection | Evidently |
| Serving | FastAPI + Pydantic |
| Orchestration | Airflow |
| CI/CD | GitHub Actions |
| Containerization | Docker + docker-compose |

## Project Status
- [ ] Phase 1: Ingestion + validation
- [ ] Phase 2: Processing + training + MLflow
- [ ] Phase 3: Drift detection + conditional retrain
- [ ] Phase 4: Serving + Docker
- [ ] Phase 5: Orchestration + CI/CD
- [ ] Phase 6: Monitoring dashboard