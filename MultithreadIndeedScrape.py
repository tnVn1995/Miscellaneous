## Sequential Scraping
from collections import defaultdict
import threading
import requests
import bs4
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import time
from typing import Callable, List, Tuple, Dict, TypeVar


def getInfo(div: BeautifulSoup) -> Dict:
    '''Take input as a bs4 tag and return a dict with information about
    a job posting
    Input
    -----
    div: list-like
        a bs4 tag of job posting
    Output
    ------
        return a dictionary with information about job title, summary link to job description,
        job location, company name'''
    temp_info = {}
    for a in div.find_all('a', attrs={'data-tn-element': 'jobTitle'}):
        temp_info['title'] = a.text
        temp_info['summarylinks'] = a['href']
    for name in div.find_all('span', attrs={'class': 'company'}):
        temp_info['name'] = name.text
    for loc in div.find_all('span', attrs={'class': 'location accessible-contrast-color-location'}):
        temp_info['location'] = loc.text
    return temp_info

##
start = time.time()
no_jobs = len(divs)
start_page = 0  # one input argument
end_page = 10  # one input argument
JobInfo = []
URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'
if start_page is not None and end_page is not None:
    for page in range(start_page, end_page):
        URL_more = URL + '&start={}'.format(page*no_jobs)
        page = requests.get(URL_more)
        print('[INFO] Getting information from the provided URL...')
        soup = BeautifulSoup(page.text, 'html.parser')
        print('[INFO] Done requesting information.')
        # Get job information from job postings
        # Loop through tag to get all the job postings in a page
        print('[INFO] Starting to scrape information ...')
        posting_tag = "jobsearch-SerpJobCard unifiedRow row result clickcard"
        divs = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
        print('[INFO] The number of job postings is:')
        no_jobss = len(divs)
        print(len(divs))
        for div in divs:
            temp_info = getInfo(div)
            JobInfo.append(temp_info)
        no_jobs = no_jobss
else:
    page = requests.get(URL)
    print('[INFO] Getting information from the provided URL...')
    soup = BeautifulSoup(page.text, 'html.parser')
    print('[INFO] Done requesting information.')
    # Get job information from job postings
    # Loop through tag to get all the job postings in a page
    print('[INFO] Starting to scrape information ...')
    # Get job information from job postings
    # Loop through tag to get all the job postings in a page
    posting_tag = "jobsearch-SerpJobCard unifiedRow row result clickcard"
    divs = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
    print(type(divs))
    for div in divs:
        temp_info = getInfo(div)
        JobInfo.append(temp_info)
data = pd.DataFrame(JobInfo)
print('The shape of the data collected is:')
print(data.shape)
print(f'[INFO] it takes {time.time() - start} secs to execute the code')
## Multithread Scraping


class MyThread(threading.Thread):
    def __init__(self, div):
        threading.Thread.__init__(self)
        self.url = div
        self.result = None

    def run(self):
        self.result = getInfo(div)


start = time.time()
no_jobs = len(divs)
start_page = 0  # one input argument
end_page = 10  # one input argument
JobInfo = []
URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'
if start_page is not None and end_page is not None:
    for page in range(start_page, end_page):
        URL_more = URL + '&start={}'.format(page*no_jobs)
        page = requests.get(URL_more)
        print('[INFO] Getting information from the provided URL...')
        soup = BeautifulSoup(page.text, 'html.parser')
        print('[INFO] Done requesting information.')
        # Get job information from job postings
        # Loop through tag to get all the job postings in a page
        print('[INFO] Starting to scrape information ...')
        posting_tag = "jobsearch-SerpJobCard unifiedRow row result clickcard"
        divs = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
        print('[INFO] The number of job postings is:')
        no_jobss = len(divs)
        print(len(divs))
        threads = [MyThread(div) for div in divs]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for thread in threads:
            JobInfo.append(thread.result)
        no_jobs = no_jobss
data = pd.DataFrame(JobInfo)
print('The shape of the data collected is:')
print(data.shape)
print(f'[INFO] it takes {time.time() - start} secs to execute the code')
else:
    page = requests.get(URL)
    print('[INFO] Getting information from the provided URL...')
    soup = BeautifulSoup(page.text, 'html.parser')
    print('[INFO] Done requesting information.')
    # Get job information from job postings
    # Loop through tag to get all the job postings in a page
    print('[INFO] Starting to scrape information ...')
    # Get job information from job postings
    # Loop through tag to get all the job postings in a page
    posting_tag = "jobsearch-SerpJobCard unifiedRow row result clickcard"
    divs = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
    print(type(divs))
    for div in divs:
        temp_info = getInfo(div)
        JobInfo.append(temp_info)
data = pd.DataFrame(JobInfo)
print('The shape of the data collected is:')
print(data.shape)
print(f'[INFO] it takes {time.time() - start} secs to execute the code')

