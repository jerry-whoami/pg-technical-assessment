# Food Delivery Time Prediction — Technical Assessment

This repository contains my submission for the **Data Science Technical Assessment**.  

## Repository Structure

```
.
├── api/                  # FastAPI prototype for real-time predictions
│   ├── main.py
│   ├── schemas.py
│   ├── service.py
│   ├── next_steps.md     # Production readiness plan
│   └── README.md         # How to run the API locally
│
├── model_pipeline/       # Data preprocessing, training, evaluation
│   ├── pipeline.py
│   ├── config.py
│   ├── notebooks/        # Jupyter notebooks for EDA & experiments
│   ├── reports/          # Written reports and reflections
│   ├── artifacts/
│   │   └── model.pkl     # Trained model artifact
│   └── data/             # Raw and testing datasets
│
├── sql/                  # SQL queries and schema files
│   ├── sql_queries.sql
│   ├── sql_insights.md
│   └── test_database/    # Seed + schema scripts
│
├── requirements.txt      # Python dependencies
└── README.md             # This file

````

## Setup & Installation

Clone the repo and create a virtual environment:

```bash
git clone https://github.com/jerry-whoami/pg-technical-assessment.git
cd pg-technical-assessment

python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
````

## Part I: SQL

Location: `sql/`

- `sql_queries.sql`: solutions to the assessment questions
- `sql_insights.md`: additional insights based on business context
- `test_database/schema_postgres.sql`: Schema for testing
- `test_database/seed_postgres.sql`: Seed data for testing

## Part II: Modeling

Location: `model_pipeline/`

- End-to-end pipeline for preprocessing, training, and evaluation
- Reports included:
  - `EDA_report.md` → exploratory data analysis
  - `model_notes.md` → model logic, metrics, tuning
  - `explainability.md` → feature importance
  - `error_insights.md` → failure analysis
  - `strategic_reflections.md` → strategic Q&A

## Part III: API Prototype (Optional)

Location: `api/`

- FastAPI service exposing:
  - `/health`: service health check
  - `/predict`: predict delivery time from input features
- `README.md` inside `api/` shows how to run locally with Python + Uvicorn
- `next_steps.md` describes what is needed for production readiness

## Deliverables Checklist

* [x] SQL queries and insights
* [x] End-to-end model pipeline
* [x] Reports and strategic reflections
* [x] API prototype with documentation
* [x] Next steps for productionization

## Notes

* Dataset: [Kaggle — Food Delivery Time Prediction](https://www.kaggle.com/datasets/denkuznetz/food-delivery-time-prediction)
* Python 3.10+