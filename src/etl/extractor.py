from api_clients.adzuna_client import AdzunaClient
from utils.logger import get_logger

class Extractor:
    def __init__(self):
        self.client = AdzunaClient()
        self.logger = get_logger(__name__)

    def extract_jobs(
        self,
        country: str = "us",
        pages: int = 1,
        results_per_page: int = 20,
    ) -> list[dict]:

        all_jobs = []
        for page in range(1, pages + 1):

           self.logger.info(
            f"Extracting jobs from Adzuna "
            f"(country={country}, page={page})"
            )

           response = self.client.search_jobs(
            country=country,
            page=page,
            results_per_page=results_per_page,
            )

           jobs = response.get("results", [])
           all_jobs.extend(jobs)

           self.logger.info(
            f"Retrieved {len(jobs)} jobs."
            )
        self.logger.info(
        f"Extracted {len(all_jobs)} jobs in total."
          )
        return all_jobs




