import requests
from typing import Dict, Any, Optional
from .config import BASE_URL, TIMEOUT, API_KEY_NAME, API_KEY_VALUE


class APIClient:
    def __init__(
        self,
        base_url: str = BASE_URL,
        api_key_name: Optional[str] = API_KEY_NAME,
        api_key_value: Optional[str] = API_KEY_VALUE,
    ):
        self.base_url = base_url
        self.api_key_name = api_key_name
        self.api_key_value = api_key_value

    def _build_headers(self) -> Dict[str, str]:
        headers = {
        }

        if self.api_key_name and self.api_key_value:
            headers[self.api_key_name] = self.api_key_value

        return headers

    def get(self, endpoint: str, params: Dict[str, Any]) -> Dict:
        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            params=params,
            headers=self._build_headers(),
            timeout=TIMEOUT
        )

        response.raise_for_status()

        return response.json()
