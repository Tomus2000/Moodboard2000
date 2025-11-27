import os
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

app_name = os.getenv("APP_NAME", "feelings-app")
app_version = os.getenv("APP_VERSION", "0.1.0")

app = FastAPI(title=app_name, version=app_version)


class EnvResponse(BaseModel):
    app_name: str
    app_version: str
    environment: str
    port: int
    log_level: str


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/env", response_model=EnvResponse)
def read_env() -> EnvResponse:
    return EnvResponse(
        app_name=os.getenv("APP_NAME", app_name),
        app_version=os.getenv("APP_VERSION", app_version),
        environment=os.getenv("ENVIRONMENT", "development"),
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info"),
    )


# To run locally: uvicorn feelings_app_env_api:app --reload --port 8000
