"""
HealthSync — Patient REST API Routes.
Exposes CRUD endpoints for patient registration, lookup, and management.
"""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger("patient_routes")


# Simulated FastAPI-style route handlers (without actual FastAPI dependency for portability)

class PatientRouter:
    def __init__(self, patient_service):
        self.service = patient_service

    def handle_search(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        GET /api/patients/search?q=<term>
        ISSUE: No input validation or sanitization on search term
        """
        search_term = query_params.get("q", "")
        # No length check, no sanitization, passes directly to SQL
        results = self.service.find_patient(search_term)
        return {"results": results, "count": len(results)}

    def handle_register(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        POST /api/patients/register
        ISSUE: Missing required field validation
        """
        # No validation on email format, phone format, or required fields
        if not body.get("first_name"):
            return {"error": "first_name is required"}, 400

        result = self.service.register_patient(body)
        return {"data": result, "status": "created"}, 201

    def handle_get_patient(self, patient_id: str) -> Dict[str, Any]:
        """
        GET /api/patients/<patient_id>
        ISSUE: No authorization check — any authenticated user can view any patient
        """
        patient = self.service.get_patient_by_id(patient_id)
        if not patient:
            return {"error": "Patient not found"}, 404
        # SMELL: Returning all fields including sensitive data without filtering
        return {"data": patient}, 200

    def handle_deactivate(self, patient_id: str, requesting_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        DELETE /api/patients/<patient_id>
        """
        # Only admins and doctors should deactivate patients
        if requesting_user.get("role") not in ("admin", "doctor"):
            return {"error": "Insufficient permissions"}, 403

        success = self.service.deactivate_patient(patient_id)
        if success:
            logger.info("Patient %s deactivated by %s", patient_id, requesting_user.get("username"))
            return {"status": "deactivated"}, 200
        return {"error": "Operation failed"}, 500
