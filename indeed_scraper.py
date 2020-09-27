"""
Project:
Module:
Authors:
Last Updated:
"""

# Load Packages:
from bs4 import BeautifulSoup
import requests
import numpy as np
from datetime import timedelta, datetime
from utils import get_digits




def get_job_description(link):
    """
    This function gets full job description given the link to the job opening.

    :param link: url to specific job listing, string
    :return: full job description, string
    """

    page = requests.get(link)
    html = BeautifulSoup(page.content, "html.parser")
    return html.find('div', id="jobDescriptionText").text


def append_job_info_dicts(job_listings, query, description=False):
    """
    Function creates a list of job info dictionaries
    :param job_listings: soup to extract information from
    :param jobs: list of dictionary to append to
    :param description: if true gets full job description
    :return: list of dictionaries containing job information
    """
    j = []
    for job in job_listings:
        # create job info dict:
        job_info = dict()

        try:
            job_info['company'] = job.find("span", class_='company').text.strip().lower()
        except AttributeError:
            job_info['company'] = 'unknown'
        job_info['id'] = job.find('div', class_='recJobLoc')['id'].split('_')[1]
        job_info['type'] = 'Full-Time' # todo: get job type from listing
        job_info['active'] = 1
        job_info['location'] = job.find('div', class_="recJobLoc")['data-rc-loc'].lower()
        job_info['position'] = job.find('a')['title'].strip().lower()
        job_info['posted'] = get_timestamp_posted(job.find('span', class_='date').text.lower())
        job_info['link'] = 'https://il.indeed.com' + job.find('a')['href']
        print(query)
        job_info['query'] = query.replace('+', ' ')
        job_info['key'] = job_info['company'] + "," + job_info['position']
        # full description or summary:
        if description:
            job_info['description'] = get_job_description(job_info['link'])
        else:
            job_info['description'] = job.find('div', class_='summary').text.strip()

        # append dictionary to job list:
        j.append(job_info)

    return j


def get_timestamp_posted(posted):
    """
    Takes a string and returns the date of the post
    :param posted: string
    :return: date
    """

    if posted == "היום":
        return datetime.timestamp(datetime.today())

    else:
        days_ago = max(get_digits(posted.split()))
        return datetime.timestamp(datetime.today() - timedelta(days=int(days_ago)))





def jobs_search(query = 'data', location='israel', days_ago=2):
    """
    Function takes a query and scrapes all the results.

    :param query: string to use in job search, string
    :param location: where to search, string
    :param days_ago: days since entry
    :return: list of dictionaries containing job information
    """
    # set main parameter for search:
    url = f"https://il.indeed.com/jobs?q={query}&l={location}&fromage={days_ago}&sort=date&filter=0" # add &start=1
    # create soup from url:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # how many jobs where found:
    search_count = soup.find(id="resultsCol").find(id="searchCountPages").text
    job_count = max([int(s) for s in search_count.replace(',', "").split() if s.isdigit()])
    page_count = int(np.ceil(job_count / 10))
    jobs = scrape_jobs_search(url, page_count, query)

    return jobs


def scrape_jobs_search(url, page_count, query):
    """

    :param url: base url with added search query
    :param page_count: number of pages found in the job search, int
    :return: list of dictionaries containing job information
    """
    # loop over all pages:
    jobs = []
    for page in range(0, page_count * 10, 10):
        print(f'scraping page number {int(page / 10)}...')

        url_page = f"{url}&start={page}"  # add &start=1
        webpage = requests.get(url_page)
        soup = BeautifulSoup(webpage.content, "html.parser")
        job_listings = soup.find(id="resultsCol").find_all('div', class_='jobsearch-SerpJobCard')
        jobs += append_job_info_dicts(job_listings, query)

    return jobs

def main():

    posted = "לפני 8 ימי"
    print(datetime.timestamp((get_date_posted(posted))))
    job_listings = jobs_search(query='data scientist', location='israel', days_ago=2)


if __name__ == "__main__":
    main()

