from datetime import datetime

from etl.extractor import Extractor
from etl.validator import Validator
from etl.transformer import Transformer
from etl.loader import Loader
from utils.logger import get_logger

logger = get_logger(__name__)

def run_etl_pipeline():
    start_time = datetime.now()
    logger.info("Starting ETL pipeline.....")

    try:
        extractor = Extractor()
        validator = Validator()
        transformer = Transformer()
        loader = Loader()

        jobs =extractor.extract_jobs(
            country="us",
            pages=5,
            results_per_page=20,
        )
        valid_jobs = validator.validate(jobs)
        transformed_data = transformer.transform(valid_jobs)
        loader.load(transformed_data)


        logger.info("ETL pipeline completed successfully.")
        logger.info(
            f"Execution Time: {datetime.now() - start_time}"
        )

    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise

def main():
    run_etl_pipeline()

if __name__ == "__main__":
    main()
    