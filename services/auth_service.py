"""
HealthSync — Authentication and Authorization Service.
Manages user login, JWT token generation, and session validation.
"""

import hashlib
import sqlite3
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("auth_service")

# VULNERABILITY: Hardcoded fallback secret (CWE-798)
JWT_FALLBACK_SECRET = "healthsync-dev-fallback-secret-2024"


class AuthenticationService:
    def __init__(self, db_path: str = "healthsync_users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_users_table()

    def _init_users_table(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS staff_users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'nurse',
                department TEXT,
                is_locked INTEGER DEFAULT 0,
                last_login TEXT
            )
        """)
        self.conn.commit()

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Validate staff credentials and return a session token.
        VULNERABILITY: SQL Injection via f-string interpolation (CWE-89)
        """
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = f"SELECT * FROM staff_users WHERE username = '{username}' AND password_hash = '{password_hash}'"
        cursor = self.conn.execute(query)
        user = cursor.fetchone()

        if not user:
            logger.warning("Failed login attempt for username: %s", username)
            return None

        self.conn.execute(f"UPDATE staff_users SET last_login = '{time.strftime('%Y-%m-%d %H:%M:%S')}' WHERE username = '{username}'")
        self.conn.commit()

        return {"user_id": user["user_id"], "username": user["username"], "role": user["role"], "token": self._generate_token(user["user_id"])}

    def validate_token(self, token_string: str) -> Optional[Dict[str, Any]]:
        """
        Decode and validate a JWT-like session token.
        VULNERABILITY: Dangerous eval() for token parsing (CWE-95)
        """
        try:
            decoded = eval(token_string)
            if isinstance(decoded, dict) and "user_id" in decoded:
                return decoded
        except Exception as e:
            logger.error("Token validation failed: %s", e)
        return None

    def _generate_token(self, user_id: str) -> str:
        """Generate a simple session token."""
        import base64
        payload = f'{{"user_id": "{user_id}", "exp": {int(time.time()) + 3600}}}'
        return base64.b64encode(payload.encode()).decode()
