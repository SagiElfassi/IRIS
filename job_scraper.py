
import os
from indeed_scraper import jobs_search
from data.database import insert_jobs, create_sqlite_db


database = os.path.join('data', 'jobs.db')

query = 'data scientist'.replace(' ', '+')
location = 'israel'
days_ago = 2

job_listing = jobs_search(query=query, location=location, days_ago=days_ago)
print(len(job_listing))
create_sqlite_db(database)
insert_jobs(database, job_listing)