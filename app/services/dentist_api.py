import requests
from app.core.config import DENTIST_API_URL, DENTIST_API_LOGIN, DENTIST_API_PASS

class DentistPlusAPI:
    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        resp = requests.post(f"{DENTIST_API_URL}/auth", json={
            "login": DENTIST_API_LOGIN,
            "pass": DENTIST_API_PASS
        })
        resp.raise_for_status()
        return resp.json()["token"]

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def get(self, endpoint, params=None):
        resp = requests.get(f"{DENTIST_API_URL}{endpoint}", headers=self._headers(), params=params)
        resp.raise_for_status()
        return resp.json()

    def post(self, endpoint, data=None):
        resp = requests.post(f"{DENTIST_API_URL}{endpoint}", headers=self._headers(), json=data)
        print(">>> Отправленный data:", data)
        print(">>> Ответ сервера:", resp.status_code, resp.text)
        resp.raise_for_status()
        return resp.json()
