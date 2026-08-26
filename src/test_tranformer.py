"""
Temporary test script for the ETL Transformer.

This script:
1. Retrieves jobs from the Adzuna API.
2. Validates the API response.
3. Transforms the validated jobs.
4. Displays a summary of the transformed entities.

Delete this file after successful testing.
"""

from api_clients.adzuna_client import AdzunaClient
from etl.validator import Validator
from etl.transformer import Transformer


def main():

    print("=" * 60)
    print("LABOR MARKET INTELLIGENCE PLATFORM")
    print("Testing Transformer Module")
    print("=" * 60)

    # Initialize components
    client = AdzunaClient()
    validator = Validator()
    transformer = Transformer()

    # ------------------------------------
    # Extract
    # ------------------------------------
    print("\nStep 1: Extracting jobs from Adzuna API...")

    raw_data = client.search_jobs(
        country="us",
        page=1,
        results_per_page=20
    )

    print(f"Retrieved {len(raw_data['results'])} jobs.")

    # ------------------------------------
    # Validate
    # ------------------------------------
    print("\nStep 2: Validating jobs...")

    valid_jobs = validator.validate(raw_data)

    print(f"Valid jobs: {len(valid_jobs)}")

    # ------------------------------------
    # Transform
    # ------------------------------------
    print("\nStep 3: Transforming jobs...")

    transformed = transformer.transform(valid_jobs)

    print("\nTransformation Summary")
    print("-" * 60)

    print(f"Companies : {len(transformed['companies'])}")
    print(f"Locations : {len(transformed['locations'])}")
    print(f"Categories: {len(transformed['categories'])}")
    print(f"Jobs      : {len(transformed['jobs'])}")

    print("\nSample Company")
    print("-" * 60)

    if transformed["companies"]:
        print(transformed["companies"][0])

    print("\nSample Location")
    print("-" * 60)

    if transformed["locations"]:
        print(transformed["locations"][0])

    print("\nSample Category")
    print("-" * 60)

    if transformed["categories"]:
        print(transformed["categories"][0])

    print("\nSample Job")
    print("-" * 60)

    if transformed["jobs"]:
        print(transformed["jobs"][0])

    print("\n" + "=" * 60)
    print("Transformer test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()