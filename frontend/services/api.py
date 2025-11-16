import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")


class ApiClient:
    """API client for communicating with the backend."""

    def __init__(self):
        self.token = None

    def login(self, email: str, password: str) -> bool:
        """Login user and store access token."""
        try:
            response = requests.post(
                f"{API_URL}/login", json={"email": email, "password": password}
            )
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
            return True
        except requests.HTTPError:
            return False

    def register(self, name: str, email: str, password: str) -> bool:
        """Register a new user."""
        try:
            response = requests.post(
                f"{API_URL}/signup",
                json={"name": name, "email": email, "password": password},
            )
            response.raise_for_status()
            return True
        except requests.HTTPError:
            return False

    def get_establishments(self):
        """Fetch list of establishments from backend."""
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = requests.get(f"{API_URL}/establishments", headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, payload: dict):
        """Generic POST request with optional token."""
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = requests.post(f"{API_URL}/{path}", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()


api_client = ApiClient()
