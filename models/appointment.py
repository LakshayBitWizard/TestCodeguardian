"""
HealthSync — Appointment Scheduling Model.
Manages doctor-patient appointment slots, statuses, and time calculations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentType(str, Enum):
    GENERAL_CHECKUP = "general_checkup"
    FOLLOW_UP = "follow_up"
    SPECIALIST = "specialist"
    EMERGENCY = "emergency"
    LAB_WORK = "lab_work"
    VACCINATION = "vaccination"


@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_id: str
    department: str
    appointment_type: AppointmentType
    scheduled_start: datetime
    duration_minutes: int = 30
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    notes: Optional[str] = None
    room_number: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def scheduled_end(self) -> datetime:
        return self.scheduled_start + timedelta(minutes=self.duration_minutes)

    def is_overlapping(self, other: "Appointment") -> bool:
        return (
            self.scheduled_start < other.scheduled_end
            and other.scheduled_start < self.scheduled_end
        )

    def cancel(self, reason: Optional[str] = None) -> None:
        self.status = AppointmentStatus.CANCELLED
        if reason:
            self.notes = f"Cancelled: {reason}" if not self.notes else f"{self.notes} | Cancelled: {reason}"

    def mark_completed(self, doctor_notes: str = "") -> None:
        self.status = AppointmentStatus.COMPLETED
        if doctor_notes:
            self.notes = f"Doctor notes: {doctor_notes}"
