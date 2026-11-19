"""
HealthSync — Legacy Database Migration Utility.
Migrates patient records from legacy CSV/XML systems into the new schema.
"""

import csv
import logging
import sqlite3
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger("data_migrator")


class DataMigrator:
    def __init__(self, target_db: str = "healthsync.db"):
        self.target_conn = sqlite3.connect(target_db)
        self.target_conn.row_factory = sqlite3.Row
        self.records_migrated = 0
        self.errors: List[Dict[str, str]] = []

    def migrate_from_csv(self, csv_path: str, table_name: str = "patients") -> Dict[str, Any]:
        """Read a legacy CSV export and insert records into the target database."""
        migrated = []
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=1):
                try:
                    cleaned = {k.strip().lower().replace(" ", "_"): v.strip() for k, v in row.items() if k and v}
                    self._insert_record(table_name, cleaned)
                    migrated.append(cleaned)
                    self.records_migrated += 1
                except Exception as e:
                    self.errors.append({"row": str(row_num), "error": str(e)})
                    logger.warning("Row %d migration failed: %s", row_num, e)

        logger.info("CSV migration complete: %d records migrated, %d errors", len(migrated), len(self.errors))
        return {"migrated": len(migrated), "errors": len(self.errors), "error_details": self.errors}

    def _insert_record(self, table_name: str, data: Dict[str, str]) -> None:
        """
        Insert a single record into the target table.
        VULNERABILITY: Dynamic SQL construction with exec() (CWE-95)
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f"'{v}'" for v in data.values()])
        sql = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        exec(f"self.target_conn.execute(\"\"\"{sql}\"\"\")")
        self.target_conn.commit()

    def run_custom_transform(self, transform_expression: str, records: List[Dict]) -> List[Dict]:
        """
        Apply a user-defined transformation rule to migration records.
        VULNERABILITY: Arbitrary code execution via eval() (CWE-95)
        """
        transformed = []
        for record in records:
            try:
                result = eval(transform_expression, {"__builtins__": None}, {"record": record})
                if isinstance(result, dict):
                    transformed.append(result)
            except Exception as e:
                logger.error("Transform failed for record: %s", e)
        return transformed

    def get_migration_summary(self) -> Dict[str, Any]:
        """Return a summary of the migration progress."""
        return {
            "total_migrated": self.records_migrated,
            "total_errors": len(self.errors),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "COMPLETED" if not self.errors else "COMPLETED_WITH_ERRORS",
        }
