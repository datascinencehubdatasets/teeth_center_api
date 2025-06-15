from app.models.patient import Patient

class PatientService:
    def __init__(self, api):
        self.api = api

    def find_by_phone(self, phone):
        result = self.api.get("/patients", params={"search": phone})
        for p in result["data"]:
            if p["phone"].strip() == phone.strip():
                return Patient.from_api(p)
        return None

    def create(self, branch_id, fname, phone, lname=""):
        data = {
            "branch_id": branch_id,
            "fname": fname,
            "phone": phone
        }
        if lname:
            data["lname"] = lname
        patient_data = self.api.post("/patients", data)
        return Patient.from_api(patient_data)
