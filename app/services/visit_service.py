from app.models.visits import Visit
from datetime import datetime, timedelta


class VisitService:
    def __init__(self, api):
        self.api = api

    def create(self, branch_id, patient_id, doctor_id, start, end, description=""):
        data = {
            "branch_id": branch_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "start": start,
            "end": end,
            "description": description
        }
        visit_data = self.api.post("/visits", data)
        return Visit.from_api(visit_data)

    def get_doctor_schedule(self, doctor_id, date):
        params = {
            "doctor_id": doctor_id,
            "date_from": date,
            "date_to": date,
            'branch_id': '7876'
        }

        return self.api.get("/schedule", params=params)

    def get_doctor_visits(self, doctor_id, date):
        params = {
            "doctor_id": doctor_id,
            "date_from": date,
            "date_to": date,
            "per_page": 100
        }
        return self.api.get("/visits", params=params)["data"]

    def find_free_slots(self, doctor_id, date, slot_minutes=30):
        schedule = self.get_doctor_schedule(doctor_id, date)

        intervals = []
        for s in schedule:
            start = datetime.strptime(
                s["day"] + " " + s["time_from"], "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(
                s["day"] + " " + s["time_to"], "%Y-%m-%d %H:%M:%S")
            intervals.append((start, end))

        visits = self.get_doctor_visits(doctor_id, date)
        busy = []
        for v in visits:
            busy_start = datetime.strptime(v["start"], "%Y-%m-%d %H:%M:%S")
            busy_end = datetime.strptime(v["end"], "%Y-%m-%d %H:%M:%S")
            busy.append((busy_start, busy_end))

        # Ищем свободные слоты
        free_slots = []
        for work_start, work_end in intervals:
            current = work_start
            busy_sorted = sorted(
                [b for b in busy if b[0] < work_end and b[1] > work_start], key=lambda x: x[0])
            for b_start, b_end in busy_sorted:
                while current + timedelta(minutes=slot_minutes) <= b_start:
                    slot_end = current + timedelta(minutes=slot_minutes)
                    if slot_end <= b_start:
                        free_slots.append({"start": current.strftime("%Y-%m-%d %H:%M:%S"),
                                           "end": slot_end.strftime("%Y-%m-%d %H:%M:%S")})
                    current = slot_end
                current = max(current, b_end)
            while current + timedelta(minutes=slot_minutes) <= work_end:
                slot_end = current + timedelta(minutes=slot_minutes)
                if slot_end <= work_end:
                    free_slots.append({"start": current.strftime("%Y-%m-%d %H:%M:%S"),
                                       "end": slot_end.strftime("%Y-%m-%d %H:%M:%S")})
                current = slot_end
        return free_slots
