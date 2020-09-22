from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from bs4 import BeautifulSoup
from random import randint

GLASS_DOOR = r"https://www.glassdoor.com/sitedirectory/title-jobs.htm"
POS = "data scientist"
LOC = "tel aviv"


def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    return webdriver.Chrome(executable_path=r'./chromedriver', options=chrome_options)


def get_rid_off_signup(driver):
    time.sleep(2)
    try:
        driver.find_element_by_class_name("jl react-job-listing gdGrid ").click()
    except ElementClickInterceptedException:
        pass


def search_jobs(keyword, location, driver):
    position_element = driver.find_element_by_id("sc.keyword")
    position_element.send_keys(keyword)
    location_element = driver.find_element_by_id("sc.location")
    location_element.send_keys(location)
    driver.find_element_by_id("HeroSearchButton").click()

    get_rid_off_signup(driver)


d = get_driver()
d.get(GLASS_DOOR)
search_jobs(POS, LOC, d)