"""
HealthSync — Application Configuration.
Loads runtime environment variables and database settings.
"""

import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    username: str = os.getenv("DB_USER", "healthsync_user")
    password: str = os.getenv("DB_PASS", "")
    database: str = os.getenv("DB_NAME", "healthsync_dev")


@dataclass
class AppConfig:
    app_name: str = "HealthSync Clinical Portal"
    environment: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
