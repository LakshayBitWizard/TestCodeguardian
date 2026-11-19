"""
HealthSync — Patient Data Model.
Defines the Patient entity structure for the clinical records system.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNDISCLOSED = "undisclosed"


class BloodType(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    O_POS = "O+"
    O_NEG = "O-"
    AB_POS = "AB+"
    AB_NEG = "AB-"


@dataclass
class Patient:
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    email: str
    phone: str
    address: str
    blood_type: Optional[BloodType] = None
    allergies: List[str] = field(default_factory=list)
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    is_active: bool = True

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def has_allergy(self, substance: str) -> bool:
        """Return whether an allergy matches ``substance``, ignoring case."""
        normalized_substance = substance.casefold()
        return any(
            allergy.casefold() == normalized_substance
            for allergy in self.allergies
        )
