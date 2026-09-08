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

    def validate(self, jobs: list[dict]) -> list[dict]:
        
        if not isinstance(jobs, list):
            raise ValueError("Jobs must be provided as a list.")
       
        valid_jobs = []

        for job in jobs:
           
           if self._is_valid_job(job):
                valid_jobs.append(job)

        self.logger.info(
              f"Validated {len(valid_jobs)} of {len(jobs)} job records."
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
            









        