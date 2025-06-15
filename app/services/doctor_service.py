from app.models.doctor import Doctor

class DoctorService:
    def __init__(self, api):
        self.api = api

    def get(self, doctor_id):
        data = self.api.get(f"/doctors/{doctor_id}")
        return Doctor.from_api(data)
