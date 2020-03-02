#%% Indeed Web Crawler
import requests
import bs4
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import time
from typing import List
import pymysql

password = '22147565Ll'

ap = argparse.ArgumentParser()
ap.add_argument('-URL', '--link', required=True,
                help='a string or a list of strings that specify the links of the job posting')
ap.add_argument('-no', '--page',
                help='The number of pages to scrape')
ap.add_argument('-fi', '--file',
                help='File to save info to')
args = vars(ap.parse_args())
## Import url
#URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'


def getJobInfo(divs: BeautifulSoup) -> (str, str, str, str):
    """Get job titles, locations, summary links, and companies' names from indeed job postings
    Input
    -----
    divs: bs4 tag
        contents of the Indeed job search results
    Output
    -----
        return titles of the jobs, companies' names, locations and job summary links of the companies from
        indeed job postings
    """
    # Get the title and summary link of the job
    job_titles = []
    summary_links = []
    names = []
    job_locations = []
    for div in divs:
        for a in div.find_all('a', attrs={'data-tn-element': 'jobTitle'}):
            job_titles.append(a['title'])
            summary_links.append(a['href'])
        # Get Company Name
        for sjcl in div.find_all('div', attrs={'class': 'sjcl'}):
            for name in sjcl.find_all('span', attrs={'class': 'company'}):
                names.append(name.text)
        # Get company locations
        for loc in div.find_all('span', attrs={'class': 'location accessible-contrast-color-location'}):
            job_locations.append(loc.text)
    return job_titles, summary_links, names, job_locations

# job_titless, summary_linkss, namess, locations = getJobInfo(divs)


##
# Job Summary link
def get_jobdes(summary_links: str, base_web='https://www.indeed.com') -> List[str]:
    """Get job descriptions from Indeed
    Input:
    -----
    summary_links: list-like
        list of connecting links
    base_web: www.indeed.com
    Output:
    -----
        Return a list-like of jobdescriptions for each link provided"""
    summaries = []
    try:
        for tail in summary_links:
            link = base_web + tail
            page = requests.get(link)
            soup = BeautifulSoup(page.text, 'html.parser')
            div = soup.find_all('div', attrs={'id': 'jobDescriptionText'})
            summaries.append(div[0].text)
    except IndexError:
        print('Here\'s what div looks like\n:', div)
    return summaries


def getJobPost(URL: str='http://www.indeed.com/jobs?', queries: dict=None) -> BeautifulSoup:
    try:
        page = requests.get(URL, params=queries)
    except Exception as e:
        print(e)
    else:
        if page == None:
            print('Not found page')
        else:
            soup = BeautifulSoup(page.text, 'html.parser')
    divs = soup.find_all(name='div', attrs={'data-tn-component': 'organicJob'})
    return divs

#%% RDB

def createdb():
    conn = pymysql.connect(host='localhost',
                    user='root',
                    password=password)
    with conn.cursor() as cur:
        cur.execute('CREATE DATABASE IF NOT EXISTS mydatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci')
        cur.execute('''CREATE TABLE IF NOT EXISTS job_hunting (id BIGINT(7) NOT NULL AUTO_INCREMENT, job_title VARCHAR(200),
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, company_name VARCHAR(200) NULL, 
    URL VARCHAR(500) NULL, location VARCHAR(200) NULL, status VARCHAR(100) NULL, applied BOOLEAN NOT NULL DEFAULT 0, PRIMARY KEY(id)) 
    CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;''')
    conn.commit()
    conn.close()

def store(values_to_insert: List[str]):
    conn = pymysql.connect(host='localhost',
                    user='root',
                    password=password)
    query = '''INSERT INTO job_hunting (job_title, company_name, URL, location) 
    VALUES''' + ",".join("(%s, %s, %s, %s)" for _ in values_to_insert)
    flattened_values = [item for sublist in values_to_insert for item in sublist]
    with conn.cursor() as cur:
        cur.execute('USE scraping')
        cur.execute(query, flattened_values)
    conn.commit()
    conn.close()

def reset_table(table: str= 'job_hunting'):
    query = f'''TRUNCATE TABLE {table}'''
    conn = pymysql.connect(host='localhost',
                    user='root',
                    password=password)
    with conn.cursor() as cur:
        cur.execute('USE scraping')
        cur.execute(query)
    conn.close()
reset_table()

def select(statement: str= '''SELECT URL FROM job_hunting''') -> str:
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password=password)
    with conn.cursor() as cur:
        cur.execute('USE scraping')
        cur.execute(statement)
        print(cur.fetchall())
    conn.close()

#%%
def main():
    start = time.time()
    # TODO: Get a list of cities, job_titles for thorough job search on Indeed
    params = {'q': 'data scientist', 'l': 'Houston, TX',
    'explvl': 'entry_level', 
    'jt':'fulltime','start': 0}
    if args['link']:
        URL = args['link']
        divs = getJobPost(URL, queries= params)
    else:
        divs = getJobPost(queries= params)
    #* Get info from job_postings from Indeed.com
    job_titles, summary_linkss, names, locations = getJobInfo(divs)
        # TODO: Get job_descriptions later for NLP project
        # TODO: summaries = get_jobdes(summary_linkss)

    #* Insert data into database
    base = 'https://www.indeed.com/'
    values_to_insert = [(job_title, company_name, base + URL, location) for job_title, company_name, URL, location in
    zip(job_titles, names, summary_linkss, locations)]
    store(values_to_insert)
    end = time.time()
    print(f'[INFO] The execution time is {(end - start) / 60} minutes')
## Execute Web Scraping
if __name__ == '__main__':
    main()
 

#%%

