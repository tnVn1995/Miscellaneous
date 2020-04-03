##
import requests
from bs4 import BeautifulSoup
from typing import TypeVar, Any, List, Callable, Dict, Generic
import pandas as pd


class Content:
    def __init__(self, name: str, url: str, jobInfo: List[Dict[str, str]]):
        self.url = url
        self.jobInfo = jobInfo
        self.name = name
        self.jobs = None

    def print(self):
        """Print out the content of the pages scraped"""
        self.jobs = pd.DataFrame(self.jobInfo)
        print(f'Scraping information from {self.name}...')
        print('the provided URL is:{}'.format(self.url))
        print('Job postings\' information:\n{}'.format(self.jobs))

    def save(self):
        print('[INFO] Saving info scraped ...')
        """Save the content into a csv file"""
        self.jobs.to_csv('Jobs.csv', index=None, header=True)


class Crawler:
    def getPage(self, url: str) -> BeautifulSoup:
        """Request content from the specified url and return a bs4 tag"""
        print('[INFO] Getting information from the provided URl...')
        try:
            res = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
        return BeautifulSoup(res.text, 'html.parser')

    def getTag(self, bs4tag: BeautifulSoup, tag: str, attribute: Dict[str, str]) -> List[str]:
        """Find the content from the tags given with specified attributes and return a bs4tag"""
        return bs4tag.find_all(tag, attrs=attribute)


class Indeed:
    def __init__(self, bs4tag: BeautifulSoup):
        self.bs4tag = bs4tag
        self.jobInfo_ = []

    def getInfo(self):
        """Getting the requested information from a bs4 tag"""
        print('[INFO] Getting job postings info ...')
        crawler = Crawler()
        for idx, div in enumerate(self.bs4tag):
            try:
                temp_info = {}
                temp_info['title'] = crawler.getTag(bs4tag=div, tag='a', attribute={'data-tn-element': 'jobTitle'})[
                    0].text
                temp_info['summary_links'] = \
                crawler.getTag(bs4tag=div, tag='a', attribute={'data-tn-element': 'jobTitle'})[0]['href']
                temp_info['company name'] = crawler.getTag(bs4tag=div, tag='span', attribute={'class': 'company'})[
                    0].text
                temp_info['location'] = crawler.getTag(bs4tag=div, tag='span', attribute={'class': 'location '
                                                                                                   'accessible'
                                                                                                   '-contrast-color'
                                                                                                   '-location'})[0].text
            except IndexError:
                print(idx)
            self.jobInfo_.append(temp_info)
        return self.jobInfo_


if __name__ == '__main__':
    # First page scrape
    Crawler = Crawler()
    URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'
    soup = Crawler.getPage(URL)
    divs = Crawler.getTag(soup, tag='dib', attribute={'data-tn-component': 'organicJob'})
    indeed = Indeed(divs)
    jobInfo = indeed.getInfo()
    # Save info scraped into a csv file
    content = Content('Indeed', URL, jobInfo)
    content.print()
    content.save()
    # More pages scrape

## Implementing Indeed Web-Scraping
crawler = Crawler()
URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'
start = time.time()
start_page = 0  # one input argument
end_page = 10  # one input argument
# JobInfo = []
print('[INFO] Getting information from the first page results...')
soup = crawler.getPage(URL)
print('[INFO] Done requesting information.')
# Get job information from job postings
# Loop through tag to get all the job postings in a page
print('[INFO] The number of job postings is:')
no_jobs = len(divs)
print(no_jobs)
print('[INFO] Starting to scrape information from job postings...')
divs = crawler.getTag(bs4tag=soup, tag='div', attribute={'data-tn-component': 'organicJob'})
indeed = Indeed(divs, crawler)
jobInfo = indeed.getInfo()
content = Content(URL, jobInfo)
content.print()
for div in divs:
    temp_info['title'] = crawler.getTag(bs4tag=div, tag='a', attribute={'data-tn-element': 'jobTitle'})[0].text
    temp_info['summary_links'] = crawler.getTag(bs4tag=div, tag='a', attribute={'data-tn-element': 'jobTitle'})[0][
        'href']
    temp_info['company name'] = crawler.getTag(bs4tag=div, tag='span', attribute={'class': 'company'})[0].text
    temp_info['location'] = \
        crawler.getTag(bs4tag=div, tag='span', attribute={'class': 'location accessible-contrast-color-location'})[
            0].text

if start_page is not None and end_page is not None:
    URLs_more = [URL + '&start={}'.format(page * no_jobs) for pag in range(start_page, end_page)]
    for idx, URL_more in enumerate(URLs_more):
        print(f'[INFO] Getting information for the next 10 results from the {idx * no_jobs}th results...')
        soup = crawler.getPage(URL_more)
        print('[INFO] Done requesting information.')
        divs = crawler.getTag(bs4tag=soup, tag='div', attribute={'data-tn-component': 'organicJob'})
        # Get job information from job postings
        # Loop through tag to get all the job postings in a page
        print('[INFO] The number of job postings is:')
        no_jobs = len(divs)
        print(no_jobs)
        print('[INFO] Starting to scrape information from job postings...')
        divs = crawler.getTag(bs4tag=soup, tag='div', attribute={'data-tn-component': 'organicJob'})
