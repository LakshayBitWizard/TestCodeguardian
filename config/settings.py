"""
HealthSync — Application Configuration and Secrets Management.
Loads database credentials, API keys, and runtime settings.
"""

import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    username: str = "healthsync_admin"
    # VULNERABILITY: Hardcoded database credentials (CWE-798)
    password: str = "HSAdmin@Prod2024!Secure"
    database: str = "healthsync_production"
    ssl_mode: str = "prefer"

    @property
    def connection_string(self) -> str:
        return (
            f"postgresql://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
            f"?sslmode={self.ssl_mode}"
        )


@dataclass
class AppConfig:
    debug: bool = True
    # VULNERABILITY: Hardcoded JWT secret key
    jwt_secret: str = "healthsync-jwt-s3cr3t-k3y-do-not-share"
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60
    max_upload_size_mb: int = 25
    allowed_origins: list = None

    def __post_init__(self):
        if self.allowed_origins is None:
            self.allowed_origins = ["*"]  # SMELL: Overly permissive CORS


@dataclass
class MailConfig:
    smtp_host: str = "smtp.healthsync.internal"
    smtp_port: int = 587
    # VULNERABILITY: Hardcoded email credentials
    smtp_user: str = "notifications@healthsync.com"
    smtp_password: str = "EmailN0tif!2024"


def load_config() -> dict:
    """Load all configuration objects with environment overrides."""
    db = DatabaseConfig(
        host=os.getenv("DB_HOST", DatabaseConfig.host),
        port=int(os.getenv("DB_PORT", str(DatabaseConfig.port))),
    )
    app = AppConfig(
        debug=os.getenv("DEBUG", "true").lower() == "true",
    )
    mail = MailConfig()

    return {"database": db, "app": app, "mail": mail}
