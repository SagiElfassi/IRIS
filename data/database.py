"""
Project:
Module:
Authors:
Last Updated:
"""


import sqlite3
import pandas as pd
import os
import csv
import tqdm
import pandas as pd


#create database
database = os.path.join('jobs.db')


def create_sqlite_db(database):
    print(database)
    if os.path.exists(database):
        os.remove(database)

    with sqlite3.connect(database) as con:
        cur = con.cursor()

        # create openings table
        cur.execute('''CREATE TABLE openings_indeed
                     ([job_id] TEXT NOT NULL
                     , [position] TEXT NOT NULL
                     , [company] TEXT NOT NULL
                     , [location] TEXT NOT NULL
                     , [type] INTEGER 
                     , [posted] TEXT NOT NULL
                     , [active] INTEGER NOT NULL
                     , [link] TEXT NOT NULL
                     , [description] TEXT NOT NULL
                     )''')

        # create a unique value to prevent duplicates:
        cur.execute('''CREATE UNIQUE INDEX idx_openings_job_id ON openings_indeed(job_id);''')

        # create openings table
        cur.execute('''CREATE TABLE employment_type
                    ([id] INTEGER NOT NULL
                    , [type] TEXT NOT NULL
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
            print(job['link'])

            # create a tuple of all values to insert into the db:
            values = (job['id'], job['position'], job['company'],
                      job['location'], job['type'], job['posted'],
                      job['active'], job['link'], job['description'])
            # execute query:
            cur.execute(f'''INSERT OR REPLACE INTO openings_indeed (job_id, position, company, 
                                             location, type, posted, 
                                             active, link, description)
                            VALUES {values};''')


def main():


    insert_jobs(database, test_job)

if __name__ == "__main__":
    main()
