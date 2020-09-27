import sqlite3
import os

# create database
database = os.path.join('data','jobs.db')


def create_sqlite_db(database):
    if os.path.exists(database):
        os.remove(database)

    with sqlite3.connect(database) as con:
        cur = con.cursor()

        # create openings table
        cur.execute('''CREATE TABLE openings_indeed
                     ([job_id] TEXT NOT NULL
                     ,[indeed_id] TEXT 
                     ,[position] TEXT NOT NULL
                     ,[company] TEXT NOT NULL
                     ,[location] TEXT NOT NULL
                     ,[type] TEXT 
                     ,[posted] timestamp
                     ,[active] INTEGER NOT NULL
                     ,[link] TEXT NOT NULL
                     ,[description] TEXT NOT NULL          
                     )''')

        # create a unique value to prevent duplicates:
        cur.execute('''CREATE UNIQUE INDEX idx_openings_job_id ON openings_indeed(job_id);''')

        # create openings table
        cur.execute('''CREATE TABLE employment_type
                    ([id] INTEGER NOT NULL
                    , [type] TEXT NOT NULL)''')

        # create user table
        cur.execute('''CREATE TABLE user
                             ([phone] integer NOT NULL
                             , [name] TEXT 
                             , [position] TEXT NOT NULL
                             , [location] TEXT NOT NULL
                             )''')


def insert_jobs(database, jobs):
    """
    function to insert job into DB. If job_id already exists, the entry is updated.

    :param database: database path/name
    :param jobs: scraped data as a list of tuples containing ()
    :return: None
    """
    with sqlite3.connect(database) as con:
        cur = con.cursor()

        # loop over scraped jobs:
        for job in jobs:
            # create a tuple of all values to insert into the db:
            values = (job['key'], job['position'], job['company'],
                      job['location'], job['type'], job['posted'],
                      job['active'], job['link'],  job['description'])


            # execute query:
            cur.execute(f'''INSERT OR REPLACE INTO openings_indeed (job_id, position, company, 
                                             location, type, posted, 
                                             active, link, description)
                            VALUES {values};''')