from sqlalchemy.orm import Session
from utils.logger import get_logger
from database.connection import engine
from sqlalchemy import select 
from database.models import (Source, Company, Location, Category, Job)


class Loader:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.engine = engine

    def load(self, transformed_data: dict):

        self.logger.info("Starting data loading process.")
        with Session(self.engine) as session:
                    try:
                        self._load_sources(session)
                        self._load_companies(session, transformed_data["companies"])
                        self._load_locations(session, transformed_data["locations"])
                        self._load_categories(session, transformed_data["categories"])

                        company_lookup = self._build_company_lookup(session)
                        location_lookup = self._build_location_lookup(session)
                        category_lookup = self._build_category_lookup(session)
                        source_lookup = self._build_source_lookup(session)

                        self._load_jobs(
                        session,
                        transformed_data["jobs"],
                        company_lookup,
                        location_lookup,
                        category_lookup,
                        source_lookup,
                    )
                        session.commit()
                        self.logger.info("Data loading completed successfully.")
                        
                    except Exception as e:
                        session.rollback()
                        self.logger.exception(
                           f"Database loading failed: {e}"
                          )
                        raise 

        
    def _load_sources(self, session: Session):

        source_name = "Adzuna"

        existing_source = session.scalar(
            select(Source).where(Source.source_name == source_name)
        )
        if existing_source is None:
            session.add(
                Source(source_name=source_name)
            )
            self.logger.info(
                f"Inserted new source: {source_name}"
            )
        else:
            self.logger.info(
                f"Source already exists: {source_name}"
            )


    def _load_companies(self, session:Session, companies: list) -> dict:

        existing_companies = {
            company.company_name
            
            for company in session.scalars(
                select(Company)
            )
        }

        inserted = 0

        for company in companies:
            company_name = company["company_name"]

            if company_name not in existing_companies:
               session.add(
                Company(company_name=company_name)
            )
               existing_companies.add(company_name)

               inserted += 1

        self.logger.info(
            f"Inserted {inserted} new company(s)."
            )
        
        
    def _load_locations(self, session: Session, locations: list) -> dict:

        existing_locations ={
            location.display_name

            for location in session.scalars(
                select(Location)
            )
        }
        inserted = 0

        for location in locations:
            display_name = location["display_name"]

            if display_name not in existing_locations:
                session.add(
                   Location(
                      country=location["country"],
                      state=location["state"],
                      county=location["county"],
                      city=location["city"],
                      display_name=display_name,
                      latitude=location["latitude"],
                      longitude=location["longitude"],
                )
                )
                existing_locations.add(display_name)

                inserted += 1

        self.logger.info(
            f"Inserted {inserted} new locations"
            )


    def _load_categories(self, session:Session, categories: list)-> dict:

        existing_categories = {
            category.category_tag

            for category in session.scalars(
                select(Category)
            )
        }

        inserted = 0

        for category in categories:

            category_tag = category["category_tag"]

            if category_tag not in existing_categories:

              session.add(
                Category(
                  category_tag = category_tag,
                  category_name = category["category_name"]
                )
            )

              existing_categories.add(category_tag)

              inserted += 1

        self.logger.info(
            f"Inserted {inserted} new categories"
            )
        

    def _build_source_lookup(self, session:Session)-> dict:

        source_lookup ={
            source.source_name: source.source_id

            for source in session.scalars(
                select(Source)
            )
        }
        self.logger.info(
            f"Built source lookup with {len(source_lookup)} entries."
        )
        return source_lookup

    def _build_company_lookup(self, session:Session)-> dict:

        company_lookup ={
            company.company_name: company.company_id

            for company in session.scalars(
                select(Company)
            )
        }
        self.logger.info(
            f"Built company lookup with {len(company_lookup)} entries."
        )
        return company_lookup

    def _build_location_lookup(self, session: Session)->dict:

        location_lookup = {
            location.display_name: location.location_id

            for location in session.scalars(
                select(Location)
            )
        }
        self.logger.info(
            f"Built location lookup with {len(location_lookup)} entries."
        )
        return location_lookup

    def _build_category_lookup(self, session: Session)-> dict:

        category_lookup = {
            category.category_tag: category.category_id

            for category in session.scalars(
                select(Category)
            )
        }
        self.logger.info(
            f"Built category lookup with {len(category_lookup)} entries."
        )
        return category_lookup
    

    def _load_jobs(self, session:Session, 
                   jobs:list, company_lookup: dict, 
                   location_lookup: dict, 
                   category_lookup: dict, 
                   source_lookup: dict
                   )-> None:
        
        incoming_job_ids = [
        job["job_id"]
        for job in jobs
        ]
        existing_jobs = {
            job.job_id: job

            for job in session.scalars(
                select(Job).where(
                    Job.job_id.in_(incoming_job_ids))
            )  
        }
        inserted = 0
        updated = 0
        unchanged = 0

        for job in jobs:
            company_id = company_lookup[job["company_name"]]
            location_id = location_lookup[job["location_display_name"]]
            category_id = category_lookup[job["category_tag"]]
            source_id = source_lookup[job["source_name"]]

            if job["job_id"] in existing_jobs:
                existing_job = existing_jobs[job["job_id"]]
                has_changed = False

                if existing_job.title != job["title"]:
                    existing_job.title = job["title"]
                    has_changed = True

                if existing_job.description != job["description"]:
                    existing_job.description = job["description"]
                    has_changed = True

                if existing_job.salary_min != job["salary_min"]:
                    existing_job.salary_min = job["salary_min"]
                    has_changed = True

                if existing_job.salary_max != job["salary_max"]:
                    existing_job.salary_max = job["salary_max"]
                    has_changed = True

                if existing_job.salary_average != job["salary_average"]:
                    existing_job.salary_average = job["salary_average"]
                    has_changed = True

                if existing_job.salary_predicted != job["salary_predicted"]:
                    existing_job.salary_predicted = job["salary_predicted"]
                    has_changed = True

                if existing_job.contract_type != job["contract_type"]:
                    existing_job.contract_type = job["contract_type"]
                    has_changed = True

                if existing_job.contract_time != job["contract_time"]:
                    existing_job.contract_time = job["contract_time"]
                    has_changed = True

                if existing_job.redirect_url != job["redirect_url"]:
                    existing_job.redirect_url = job["redirect_url"]
                    has_changed = True

                if existing_job.adref != job["adref"]:
                    existing_job.adref = job["adref"]
                    has_changed = True

                if has_changed:
                   updated += 1
                else:
                   unchanged += 1
                continue

            company_id = company_lookup[
                job["company_name"]
            ]
            location_id = location_lookup[
                job["location_display_name"]
            ]
            category_id = category_lookup[
                job["category_tag"]
            ]
            source_id = source_lookup[
                job["source_name"]
            ]

            session.add(
                Job(
                     job_id=job["job_id"],
                     title=job["title"],
                     description=job["description"],
                     salary_min=job["salary_min"],
                     salary_max=job["salary_max"],
                     salary_average=job["salary_average"],
                     salary_predicted=job["salary_predicted"],
                     contract_type=job["contract_type"],
                     contract_time=job["contract_time"],
                     created_date=job["created_date"],
                     redirect_url=job["redirect_url"],
                     adref=job["adref"],
                     company_id = company_id,
                     location_id = location_id,
                     category_id = category_id,
                     source_id = source_id
                )
            )
        
            inserted += 1
        self.logger.info(
    f"Jobs processed: "
    f"{inserted} inserted, "
    f"{updated} updated, "
    f"{unchanged} unchanged."
)
        




















