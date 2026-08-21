from config import Config
import requests

class AdzunaClient:
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"
    def __init__(self):
        self.app_id = Config.AZDUNA_APP_ID
        self.app_key = Config.AZDUNA_APP_KEY

        if not self.app_id or not self.app_key:
            raise ValueError( 
                "Adzuna credentials not found" 
                "Please configure your .env file."
            )
        self.session = requests.Session()

    """def test_connection(self):
        print("Adzuna Client initialized successfully.")
        print(f"App ID: {self.app_id}")"""

    def search_jobs(self, country="us", page=1, results_per_page=10):
        endpoint = (
            f"{self.BASE_URL}/{country}/search/{page}"
                   )
        params = {
           "app_id": self.app_id,
           "app_key": self.app_key,
           "results_per_page": results_per_page,
                 }
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

















    