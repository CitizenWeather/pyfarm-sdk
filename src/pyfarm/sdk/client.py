"""Typed HTTP client for pyfarm-api."""
from __future__ import annotations

from typing import Any

import httpx
from pydantic import BaseModel


class GrowData(BaseModel):
    """Grow record model."""

    grow_id: str
    crop_type: str
    stage: int
    status: str


class PyFarmClient:
    """Typed async HTTP client for pyfarm-api.

    Usage:
        client = PyFarmClient("http://localhost:8000")
        grow = await client.get_grow("grow-1")
        await client.set_sensor_reading("temp-1", 25.5)
    """

    def __init__(
        self,
        api_base: str = "http://localhost:8000",
        timeout: float = 30.0,
        auth_token: str | None = None,
    ) -> None:
        self.api_base = api_base.rstrip("/")
        self.timeout = timeout
        self.auth_token = auth_token
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Lazy-initialize async HTTP client."""
        if not self._client:
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            self._client = httpx.AsyncClient(
                base_url=self.api_base,
                timeout=self.timeout,
                headers=headers,
            )
        return self._client

    async def close(self) -> None:
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get_grow(self, grow_id: str) -> GrowData:
        """Retrieve grow record."""
        client = await self._get_client()
        response = await client.get(f"/grows/{grow_id}")
        response.raise_for_status()
        return GrowData(**response.json())

    async def list_grows(self, limit: int = 100) -> list[GrowData]:
        """List grows."""
        client = await self._get_client()
        response = await client.get("/grows", params={"limit": limit})
        response.raise_for_status()
        return [GrowData(**g) for g in response.json()]

    async def set_sensor_reading(
        self,
        sensor_id: str,
        value: float,
        metric: str = "default",
        unit: str = "unit",
    ) -> None:
        """Record a sensor reading."""
        client = await self._get_client()
        payload = {"sensor_id": sensor_id, "metric": metric, "value": value, "unit": unit}
        response = await client.post("/sensor-readings", json=payload)
        response.raise_for_status()

    async def get_sensor_readings(
        self,
        sensor_id: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Retrieve recent sensor readings."""
        client = await self._get_client()
        response = await client.get(
            f"/sensor-readings/{sensor_id}",
            params={"limit": limit},
        )
        response.raise_for_status()
        return response.json()
