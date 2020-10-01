import os
from data.database import insert_jobs, create_sqlite_db
from glassdoor_scraper import get_jobs
from indeed_scraper import jobs_search

POS = "data scientist"
LOC = "Tel Aviv"


def main():
    DB = os.path.join('data', 'jobs.db')
    create_sqlite_db(DB)

    indeed_jobs = jobs_search(query=POS.replace(' ', '+'), location=LOC.replace(' ', '+'), days_ago=2)
    insert_jobs(DB, indeed_jobs)

    glassdoor_jobs = get_jobs(keyword=POS, location=LOC)
    insert_jobs(DB, glassdoor_jobs)


if __name__ == "__main__":
    main()