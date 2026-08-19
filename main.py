from src.api_clients.adzuna_client import AdzunaClient
import json
from pathlib import Path


client = AdzunaClient()
client.test_connection()
jobs = client.search_jobs()


raw_data_path = Path("data/raw")

output_file = raw_data_path / "sample_response.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(jobs, file, indent=4)

print(f"API response saved to: {output_file}")



