from etl.extractor import Extractor
from etl.validator import Validator
from etl.transformer import Transformer
from etl.loader import Loader


def main():

    print("LABOR MARKET INTELLIGENCE PLATFORM")
    print("Testing ETL Module")

    print("\nStep 1: Extracting jobs from Adzuna API...")

    extractor = Extractor()

    jobs = extractor.extract_jobs(
    country="us",
    results_per_page=20,
           )

    print(f"Retrieved {len(jobs)} jobs.")

    print("\nStep 2: Validating jobs...")

    job_validator = Validator()

    valid_jobs = job_validator.validate(jobs)

    print(f"Valid jobs: {len(valid_jobs)}")

    print("\nStep 3: Transforming jobs...")

    job_transformer = Transformer()

    transformed_data = job_transformer.transform(valid_jobs)

    print("Transformation completed successfully.")

    print("\nStep 4: Loading data into MySQL...")

    loader = Loader()

    loader.load(transformed_data)

    print("Data loaded successfully.")
if __name__ == "__main__":
    main()