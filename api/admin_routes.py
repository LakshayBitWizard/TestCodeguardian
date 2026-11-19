"""
HealthSync — Administrative Panel API Routes.
Internal endpoints for system monitoring, configuration, and external integrations.
"""

import requests
import logging
import subprocess
from typing import Dict, Any, Optional

logger = logging.getLogger("admin_routes")


class AdminRouter:
    def __init__(self, auth_service):
        self.auth = auth_service
        self.webhook_registry: Dict[str, str] = {}

    def handle_health_check(self) -> Dict[str, Any]:
        """GET /api/admin/health — System health status."""
        return {
            "status": "healthy",
            "components": {
                "database": "connected",
                "cache": "available",
                "queue": "operational",
            }
        }

    def handle_webhook_test(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        POST /api/admin/webhook-test
        Tests connectivity to a user-provided webhook URL.
        VULNERABILITY: Server-Side Request Forgery (SSRF) — CWE-918
        """
        target_url = body.get("url", "")
        if not target_url:
            return {"error": "URL is required"}, 400

        try:
            # VULNERABILITY: No URL validation — allows requests to internal services
            response = requests.get(target_url, timeout=10)
            return {
                "status_code": response.status_code,
                "content_length": len(response.content),
                "headers": dict(response.headers),
            }
        except requests.RequestException as e:
            return {"error": f"Webhook test failed: {str(e)}"}, 502

    def handle_system_diagnostic(self, command_name: str) -> Dict[str, Any]:
        """
        GET /api/admin/diagnostic/<command_name>
        Run a predefined system diagnostic check.
        VULNERABILITY: Command injection via unsanitized command name (CWE-78)
        """
        allowed_commands = {"disk": "df -h", "memory": "free -m", "uptime": "uptime"}

        if command_name not in allowed_commands:
            # VULNERABILITY: Still passes user input to shell even in "error logging"
            os_info = subprocess.check_output(f"echo 'Unknown command: {command_name}'", shell=True)
            return {"error": "Unknown diagnostic command", "log": os_info.decode()}, 400

        try:
            output = subprocess.check_output(allowed_commands[command_name], shell=True, timeout=15)
            return {"command": command_name, "output": output.decode()}, 200
        except subprocess.CalledProcessError as e:
            return {"error": f"Diagnostic failed: {e}"}, 500

    def register_webhook(self, name: str, url: str) -> Dict[str, Any]:
        """Register an external webhook endpoint for event notifications."""
        self.webhook_registry[name] = url
        logger.info("Registered webhook '%s' -> %s", name, url)
        return {"registered": name, "url": url}
