"""NEPViewer API Client."""
from __future__ import annotations

import logging
import hashlib
import time
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://api.nepviewer.net/v2"
LOGIN_URL = f"{BASE_URL}/sign-in"
OVERVIEW_URL = f"{BASE_URL}/site/overview"


def _make_sign(email: str, password: str) -> str:
    """Generate sign string for NEP API requests.
    
    The sign is an MD5 of email+password+timestamp (rounded to hour).
    This was reverse-engineered from the web app.
    """
    ts = str(int(time.time() // 3600))
    raw = f"{email}{password}{ts}"
    return hashlib.md5(raw.encode()).hexdigest()


class NEPViewerAPI:
    """Handles all communication with the NEPViewer cloud API."""

    def __init__(self, email: str, password: str, plant_id: str) -> None:
        self._email = email
        self._password = password
        self._plant_id = plant_id
        self._token: str | None = None
        self._session: aiohttp.ClientSession | None = None

    def _get_headers(self, with_auth: bool = False) -> dict[str, str]:
        sign = _make_sign(self._email, self._password)
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "app": "0",
            "client": "web",
            "lan": "3",
            "oem": "NEP",
            "sign": sign,
        }
        if with_auth and self._token:
            headers["Authorization"] = self._token
        return headers

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def async_login(self) -> bool:
        """Login and store token. Returns True on success."""
        session = await self._get_session()
        payload = {"account": self._email, "password": self._password}
        try:
            async with session.post(
                LOGIN_URL,
                json=payload,
                headers=self._get_headers(),
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status != 200:
                    _LOGGER.error("NEPViewer login failed, HTTP %s", resp.status)
                    return False
                data = await resp.json()
                _LOGGER.debug("NEPViewer login response: %s", data)
                token = (
                    data.get("data", {})
                    .get("tokenInfo", {})
                    .get("token")
                )
                if not token:
                    _LOGGER.error("No token in NEPViewer response: %s", data)
                    return False
                self._token = token
                return True
        except aiohttp.ClientError as err:
            _LOGGER.error("NEPViewer connection error: %s", err)
            return False

    async def async_get_overview(self) -> dict[str, Any] | None:
        """Fetch plant overview. Re-logs in if needed."""
        if not self._token:
            if not await self.async_login():
                return None

        session = await self._get_session()
        payload = {"sid": self._plant_id}
        try:
            async with session.post(
                OVERVIEW_URL,
                json=payload,
                headers=self._get_headers(with_auth=True),
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 401:
                    # Token expired – re-login once
                    self._token = None
                    if not await self.async_login():
                        return None
                    async with session.post(
                        OVERVIEW_URL,
                        json=payload,
                        headers=self._get_headers(with_auth=True),
                        timeout=aiohttp.ClientTimeout(total=15),
                    ) as resp2:
                        return await resp2.json()
                if resp.status != 200:
                    _LOGGER.error("NEPViewer overview failed, HTTP %s", resp.status)
                    return None
                return await resp.json()
        except aiohttp.ClientError as err:
            _LOGGER.error("NEPViewer connection error during overview: %s", err)
            return None

    async def async_close(self) -> None:
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
