from typing import List, Dict, Any, Optional
from .client import APIClient


class APIFetcher:
    def __init__(self, client: APIClient):
        self.client = client

    def fetch_all(
        self,
        endpoint: str,
        base_params: Dict[str, Any],
        page_param: str = "pagina",
        start_page: int = 1,
        max_pages: Optional[int] = None,
    ) -> List[Dict]:

        results = []
        page = start_page

        while True:
            params = {**base_params, page_param: page}

            data = self.client.get(endpoint, params)

            # Adaptable según API
            records = data if isinstance(data, list) else data.get("data", [])

            if not records:
                break

            results.extend(records)

            page += 1

            if max_pages and page > max_pages:
                break

        return results
