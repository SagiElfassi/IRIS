from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup

GLASSDOOR = r"https://www.glassdoor.com/sitedirectory/title-jobs.htm"
TODAY = date.today()


def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    return webdriver.Chrome(executable_path=r'./chromedriver', options=chrome_options)


def get_rid_off_signup(driver):
    time.sleep(4)

    try:
        driver.find_element_by_class_name("selected").click()
    except ElementClickInterceptedException:
        pass

    time.sleep(3)

    try:
        driver.find_element_by_id("prefix__icon-close-1").click()
    except NoSuchElementException:
        pass

    return driver


def get_num_results(driver):
    raw_text = driver.find_element_by_xpath('.//div[@class="hideHH css-19rczgc e15r6eig0"]').text
    return int(raw_text.split(" ")[0])


def get_days_old(driver):
    days_old = []
    curr_page = BeautifulSoup(driver.page_source, 'html.parser')
    raw_days = curr_page.find_all("div", class_="d-flex align-items-end pl-std css-mi55ob")
    for raw in raw_days:
        days_old.append(raw.text)
    return days_old


def get_time_delta(delta):
    num = delta[:-1]
    units = delta[-1:]
    if units == 'h':
        return 0
    else:
        return int(num)


def get_url_if_possible(driver):
    try:
        return driver.find_element_by_xpath('.//div[@class="applyCTA gdGrid"]/a').get_attribute("href")
    except:
        return "Apply from glassdoor"


def clean_cmp_name(driver):
    tmp_cmp_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text.lower()
    return tmp_cmp_name.split('\n')[0]


def get_job_data(driver):
    num_jobs = get_num_results(driver)
    jobs = []
    while True:
        job_buttons = driver.find_elements_by_class_name("jl")
        days_old = get_days_old(driver)
        for i, job_button in enumerate(job_buttons):
            job_button.click()
            time.sleep(4)
            collected_successfully = False
            while not collected_successfully:
                try:
                    company_name = clean_cmp_name(driver)
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text.lower()
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text.lower()
                    job_date = TODAY - timedelta(get_time_delta(days_old[i]))
                    job_url = get_url_if_possible(driver)
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            jobs.append({"key": company_name+","+job_title,
                         "position": job_title,
                         "company": company_name,
                         "location": location,
                         "posted": str(job_date),
                         "link": job_url,
                         "description": "job_description",
                         "active": 1,
                         "type": "FULL-TIME"})

        if len(jobs) == num_jobs:
            break
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            time.sleep(2)
        except NoSuchElementException:
            break

    return jobs


def get_jobs(keyword, location):
    '''
    :param keyword: [str] search by this keyword
    :param location: [str] search by this location
    :return: [dictionary] of job rsults from glassdoor
    '''
    driver = get_driver()
    driver.get(GLASSDOOR)
    position_element = driver.find_element_by_id("sc.keyword")
    position_element.send_keys(keyword)
    location_element = driver.find_element_by_id("sc.location")
    location_element.send_keys(location)
    driver.find_element_by_id("HeroSearchButton").click()

    driver = get_rid_off_signup(driver)
    jobs = get_job_data(driver)

    return jobs


