from utils.logger import get_logger
from datetime import datetime

class Transformer:
    def __init__(self):
        self.logger = get_logger(__name__)
        

    def transform(self, validated_jobs: list) -> list:
        companies = self._transform_companies(validated_jobs)
        locations = self._transform_locations(validated_jobs)
        categories = self._transform_categories(validated_jobs)
        jobs = self._transform_jobs(validated_jobs)

        self.logger.info("Transformation completed successfully.")

        return {
            "companies": companies,
            "locations": locations,
            "categories": categories,
            "jobs": jobs,
        }
    
    
    def _transform_companies(self, jobs: list) -> dict:

        unique_companies = {}

        for job in jobs:
            company_name = job["company"]["display_name"].strip()

            if company_name not in unique_companies:
                unique_companies[company_name] ={
                    "company_name" : company_name,
                }

        self.logger.info(
        f"Extracted {len(unique_companies)} unique companies."
             )
        return list(unique_companies.values())

    def _transform_locations(self, jobs: list) -> dict:

        unique_locations = {}

        for job in jobs:

            location = job["location"]

            area = location.get("area", [])

            country = area[0] if len(area) > 0 else None
            state = area[1] if len(area) > 1 else None
            county = area[2] if len(area) > 2 else None
            city = area[3] if len(area) > 3 else None

            display_name = location["display_name"].strip()

            if display_name not in unique_locations:

                unique_locations[display_name] = {
                    "country": country,
                    "state": state,
                    "county": county,
                    "city": city,
                    "display_name": display_name,
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude"),
                }
        self.logger.info(
            f"Extracted {len(unique_locations)} unique locations."
        )
        return list(unique_locations.values())
    

    def _transform_categories(self, jobs: list) -> dict:

        unique_categories ={}

        for job in jobs:

            category = job["category"]
            category_tag = category["tag"].strip()
            category_name = category["label"].strip()

            if category_tag not in unique_categories:

                unique_categories[category_tag] ={
                    "category_tag": category_tag,
                    "category_name": category_name
                }
        self.logger.info(
            f"Extracted {len(unique_categories)} unique categories."
        )
        return list(unique_categories.values())

    def _transform_jobs(self, jobs : list) -> dict:

        unique_jobs = []

        for job in jobs:

            salary_min = job.get("salary_min")
            salary_max = job.get("salary_max")
            salary_average = None


            if salary_min is not None and salary_max is not None:
                 salary_average = (salary_min + salary_max) / 2

            created_date = None
            if job.get("created"):
                created_date = datetime.strptime(
                job["created"],
                "%Y-%m-%dT%H:%M:%SZ",
            )

            unique_jobs.append ({
                "job_id": job["id"],
                "title": job["title"],
                "description" :job["description"],
                "salary_min": salary_min,
                "salary_max": salary_max,
                "salary_average": salary_average,
                "salary_predicted": bool(
                     job.get("salary_is_predicted", 0)
                   ),
                "contract_type" : job.get("job_contract_type"),
                "contract_time" : job.get("job_contract_time"),
                "created_date": created_date,
                "redirect_url": job.get("redirect_url"),
                "adref": job.get("adref"),
                "company_name": job["company"]["display_name"],
                "location_display_name":
                     job["location"]["display_name"],
                "category_tag":
                     job["category"]["tag"],
                "source_name": "Adzuna",
                })
        self.logger.info(
            f"Extracted {len(unique_jobs)} unique job titles."
        )
        return list(unique_jobs)













    