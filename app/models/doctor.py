from pydantic import BaseModel
from typing import Optional, List, Dict

class Doctor(BaseModel):
    id: int
    fname: str
    lname: Optional[str] = ""
    branches: List[dict] = []

    @classmethod
    def from_api(cls, data):
        return cls(
            id=data["id"],
            fname=data["fname"],
            lname=data.get("lname", ""),
            branches=data.get("branches", [])
        )