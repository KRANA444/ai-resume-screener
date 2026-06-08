# AI Resume Screener — Deployment

This repository contains a Streamlit app in `app.py` that analyzes resumes against a job description.

Quick deployment options:

- Docker (recommended):
  - Build: `docker build -t ai-resume-screener .`
  - Run: `docker run -p 8501:8501 ai-resume-screener`

- Streamlit Community Cloud:
  - Push this repo to GitHub and create a new app on Streamlit Cloud.
  - It will install dependencies from `requirements.txt` and run `app.py`.

- Heroku-like platforms:
  - Push to a Git repo and ensure `Procfile` and `requirements.txt` are present.

Notes:
- The Docker image downloads the spaCy model at build time.
- Installing `sentence-transformers` pulls `torch` and other ML deps; the Docker build may take several minutes.

Next steps:
- Build the Docker image locally, or tell me which cloud to deploy to and I can prepare deploy commands.