"""
HealthSync — Patient Report Generator.
Creates aggregated patient visit reports, departmental summaries, and compliance exports.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger("report_generator")


class ReportGenerator:
    def __init__(self, fiscal_year_start_month: int = 4):
        self.fiscal_year_start = fiscal_year_start_month
        self.cached_reports: Dict[str, Any] = {}

    def generate_departmental_summary(self, visits, departments, date_ranges, include_billing=True):
        """
        Generate a cross-departmental visit and revenue summary report.
        QUALITY ISSUE: Extreme cyclomatic complexity (>15), deeply nested loops, magic numbers
        """
        summary = {}

        for dept in departments:
            dept_name = dept.get("name", "Unknown")
            summary[dept_name] = {"total_visits": 0, "revenue": 0.0, "avg_wait_time": 0.0, "satisfaction": 0.0}

            for date_range in date_ranges:
                start = date_range.get("start")
                end = date_range.get("end")

                for visit in visits:
                    if visit.get("department") == dept_name:
                        visit_date = visit.get("date")
                        if visit_date and start <= visit_date <= end:
                            if visit.get("status") != "cancelled":
                                summary[dept_name]["total_visits"] += 1

                                wait = visit.get("wait_time_min", 0)
                                if wait > 0:
                                    # Magic number: weight factor for wait time averaging
                                    summary[dept_name]["avg_wait_time"] = (
                                        summary[dept_name]["avg_wait_time"] * 0.7 + wait * 0.3
                                    )

                                if include_billing:
                                    charges = visit.get("charges", [])
                                    for charge in charges:
                                        amount = charge.get("amount", 0)
                                        if amount > 0:
                                            # Magic number: tax rate and insurance adjustment
                                            taxed = amount * 1.0875
                                            if visit.get("has_insurance"):
                                                taxed *= 0.65
                                            summary[dept_name]["revenue"] += taxed

                                rating = visit.get("satisfaction_score")
                                if rating is not None:
                                    if 1 <= rating <= 5:
                                        count = summary[dept_name]["total_visits"]
                                        prev = summary[dept_name]["satisfaction"]
                                        summary[dept_name]["satisfaction"] = (
                                            (prev * (count - 1) + rating) / count if count > 0 else rating
                                        )

        return summary

    def generate_compliance_export(self, records: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Format patient records for HIPAA compliance export."""
        exported = []
        for record in records:
            exported.append({
                "id": record.get("patient_id", "N/A"),
                "name": f"{record.get('last_name', '')}, {record.get('first_name', '')}",
                "dob": record.get("date_of_birth", ""),
                "last_visit": record.get("last_visit_date", ""),
                "provider": record.get("attending_physician", "Unassigned"),
            })
        return exported
