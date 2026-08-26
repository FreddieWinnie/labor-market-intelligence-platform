from utils.logger import get_logger

class Validator:
    Required_fields = [
                "id", 
                "title", 
                "company",
                "location", 
                "category", 
                ]
     
    def __init__(self):
        self.logger = get_logger(__name__)

    def validate(self, raw_data: dict) -> bool:
       if not isinstance(raw_data, dict):
            raise ValueError("API response must be a dictionary.")
       if "results" not in raw_data:
            raise ValueError("API response does not contain 'results'.")
       if not isinstance(raw_data["results"], list):
            raise ValueError("'results' must be a list.")
       
       valid_jobs = []
       for job in raw_data["results"]:
           if self._is_valid_job(job):
                valid_jobs.append(job)
       self.logger.info(
            f"Validated {len(valid_jobs)} of"
            f" {len(raw_data['results'])} job records."
        )
       return valid_jobs

    def _is_valid_job(self, job: dict) -> bool:
        for field in self.Required_fields:
            if field not in job:
                self.logger.warning(
                    f"Job skipped because '{field}' is missing."
                )
                return False
        if "display_name" not in job["company"]:
            self.logger.warning(
                "Job skipped because 'company.display_name' is missing."
            )
            return False
            
        if "display_name" not in job["location"]:
            self.logger.warning(
                "Job skipped because location.display_name is missing."
            )
            return False    
               
        if "tag" not in job["category"]:
            self.logger.warning(
                "Job skipped because 'category.tag' is missing."
            )
            return False

        if "label" not in job["category"]:
            self.logger.warning(
                "Job skipped because 'category.label' is missing."
            )
            return False
        return True
            









        