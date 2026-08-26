from api_clients.adzuna_client import AdzunaClient


class Extractor:
    def __init__(self):
        self.client = AdzunaClient()

    def extract_jobs(
        self,
        country: str = "us",
        page: int = 1,
        results_per_page: int = 10,
    ) -> dict:
        
        return self.client.search_jobs(
            country=country,
            page=page,
            results_per_page=results_per_page,
        )





