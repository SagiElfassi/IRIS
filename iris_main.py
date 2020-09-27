import os
from data.database import write_jobs, create_sqlite_db
from glassdoor_scraper import get_jobs

POS = "data analyst"
LOC = "tel aviv"


def main():
    DB = os.path.join('jobs.db')
    create_sqlite_db(DB)

    glassdoor_jobs = get_jobs(keyword=POS, location=LOC)
    write_jobs(DB, glassdoor_jobs)


if __name__ == "__main__":
    main()