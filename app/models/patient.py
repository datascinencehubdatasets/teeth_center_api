from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    id: int
    fname: str
    lname: Optional[str] = ""
    phone: str

    @classmethod
    def from_api(cls, data):
        return cls(
            id=data["id"],
            fname=data["fname"],
            lname = data.get("lname", ""),
            phone = data["phone"]
        )