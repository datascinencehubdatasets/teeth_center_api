from pydantic import BaseModel
from typing import Optional

class Visit(BaseModel):
    id: int
    start: str
    end: str
    doctor_id: int
    patient_id: int
    branch_id: int
    description: Optional[str] = ""

    @classmethod
    def from_api(cls, data):
        return cls(
            id=data["id"],
            start=data["start"],
            end=data["end"],
            doctor_id=data["doctor"]["id"],
            patient_id=data["patient"]["id"],
            branch_id=data["branch_id"],
            description=data.get("description", "")
        )