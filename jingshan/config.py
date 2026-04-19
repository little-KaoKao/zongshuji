from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "runs.db"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ASSETS_DIR = PROJECT_ROOT / "assets"
MODELS_TOML = PROJECT_ROOT / "models.toml"


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    poll_interval: float
    poll_timeout: float


def load_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.environ.get("RUNNINGHUB_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "RUNNINGHUB_API_KEY 未设置。请复制 .env.example 为 .env 并填入 key。"
        )
    return Settings(
        api_key=api_key,
        base_url=os.environ.get("RUNNINGHUB_BASE_URL", "https://www.runninghub.cn").rstrip("/"),
        poll_interval=float(os.environ.get("RH_POLL_INTERVAL", "5")),
        poll_timeout=float(os.environ.get("RH_POLL_TIMEOUT", "1800")),
    )
