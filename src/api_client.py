import os
import time
import httpx
from nexuscore_client import AuthenticatedClient, Client

TOKEN_URL = "http://nexuscore:8000/api/auth/token"
CLIENT_ID = os.environ.get("NEXUSCORE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("NEXUSCORE_CLIENT_SECRET")

class ManagedAPIClient:
    def __init__(self):
        self._token: str | None = None
        self._expires_at: float = 0
        self._client: AuthenticatedClient | None = None

    async def _refresh(self):
        async with httpx.AsyncClient() as http:
            resp = await http.post(TOKEN_URL, data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            })
            data = resp.json()
            self._token = data["access_token"]
            self._expires_at = time.time() + data.get("expires_in", 3600)
            self._client = AuthenticatedClient(
                base_url="http://nexuscore:8000/api",
                token=self._token
            )

    async def get(self) -> AuthenticatedClient:
        if time.time() >= self._expires_at - 30:  # refresh 30s before expiry
            await self._refresh()
        return self._client