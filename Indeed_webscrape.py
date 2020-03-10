#%% Indeed Web Crawler
import requests
import bs4
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import time
from typing import List, Tuple
#%%

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

#%%
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
    """[Get list of job postings from indeed]
    
    Keyword Arguments:
        URL {str} -- [Can be modified to scrape from other sites] 
        (default: {'http://www.indeed.com/jobs?'})
        queries {dict} -- [queries to scrape] (default: {None})
    
    Returns:
        BeautifulSoup -- [description]
    """    
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

def execute(statement: str, db: str='scraping', create=False, password = '22147565Ll'):
    conn = pymysql.connect(host='localhost',
                    user='root',
                    password=password)
    with conn.cursor() as cur:
            cur.execute(f'CREATE DATABASE IF NOT EXISTS {db}')
            cur.execute(f'USE {db}')
            cur.execute('CREATE TABLE IF NOT EXISTS test')
            cur.execute('CREATE TABLE IF NOT EXISTS test1')
    conn.commit()
    conn.close()
    return db
db = 'scraping'
conn = pymysql.connect(host='localhost',
                user='root',
                password=password)
with conn.cursor() as cur:
        cur.execute(f'CREATE DATABASE IF NOT EXISTS {db};')
        cur.execute(f'USE {db};')
        cur.execute('CREATE TABLE IF NOT EXISTS test (lol SMALLINT);')
        cur.execute('CREATE TABLE IF NOT EXISTS test1 (lol1 SMALLINT);')
        cur.execute('SHOW tables;')
        print(cur.fetchall())
conn.commit()
conn.close()

#%%

divs = getJobPost(queries= params)
#* Get info from job_postings from Indeed.com
job_titles, summary_links, company_names, locations = getJobInfo(divs)
# TODO: Get job_descriptions later for NLP project
summaries = get_jobdes(summary_links)

values_to_insert = [job_titles, summary_links, company_names, locations, summary_links]
def store(values_to_insert: List[str], password='22147565Ll^'):
    conn = pymysql.connect(host='localhost',
                    user='root',
                    password=password)

    job_titles, summary_links, company_names, locations, summaries = values_to_insert              
    # query = '''INSERT INTO job_hunting (job_title, company_name, URL, location) 
    # VALUES''' + ",".join("(%s, %s, %s, %s)" for _ in values_to_insert)
    # flattened_values = [item for sublist in values_to_insert for item in sublist]
    with conn.cursor() as cur:
        for job_title, summary_link, company_name, location, job_description in zip(job_titles, summary_links, company_names, locations, summaries):
            city, state = location.split(',')
            statement = f'''BEGIN;
    INSERT INTO job_hunting1 (company_name, city, job_title, createdDate, state, url)
    VALUES({company_name}, {city}, {job_title}, curdate(), {state}, {summary_link});
    INSERT INTO job_status (company_id) 
    VALUES(LAST_INSERT_ID());
    INSERT INTO job_desc (company_id, job_description)
    Values(LAST_INSERT_ID(), {job_description})
    COMMIT;'''  
        cur.execute('USE scraping')
        cur.execute(statement)
    conn.commit()
    conn.close()

store(values_to_insert)


#%%
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
#%% SELECT and siplay info from table in pandas Dataframe
def selectTable(items: str = '*', table: str = 'job_hunting1', db: str = 'scraping',
password: str = '22147565Ll') -> str:
    """    [Select items from table in mysql scraping db]
    
    Keyword Arguments:
        items {str} -- [items to get from table] (default: {'*'})
        table {str} -- [name of the table] (default: {'job_hunting1'})
        db {str} -- [name of the database] (default: {'scraping'})
        password {str} -- [password of the user] (default: {'22147565Ll^'})
    Returns:
        str -- [table of info]
    """    
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password=password)
    statement = f'''SELECT {items} FROM {table}'''
    with conn.cursor() as cur:
        cur.execute(f'USE {db}')
        cur.execute(statement)
        result = cur.fetchall()
    conn.close()
    return result

def displaySelect():
    job_status = 'job_status'
    job_desc = 'job_desc'
    desc = selectTable(table=job_desc)
    status = selectTable(table=job_status)
    hunting = selectTable()
    result = [desc, status, hunting]
    job_hunting_columns = ['company_id', 'company_name','createdDate','city','state','url']
    job_status_columns = ['company_id','status','createdDate']
    job_desc_columns = ['company_id','job_description','createdDate']
    # Slect job_desc
    try:
        job_hunting1 = pd.DataFrame(list(result[2]), columns=job_hunting_columns)
        job_status = pd.DataFrame(list(result[1]), columns=job_status_columns)
        job_des = pd.DataFrame(list(result[0]), columns=job_desc_columns)
    except Exception as e:
        print(e)
    return job_hunting1, job_status, job_des


job_hunting1, job_status, job_desc = displaySelect()

print(job_hunting1)
print(job_status)
print(job_desc)

#%%
from sqlalchemy import create_engine
import pymysql
import pandas as pd
# db_connection_str = 'mysql+pymysql://<root@127.0.0.1:22147565Ll^@localhost/scraping'
# db_connection = create_engine(db_connection_str)
import mysql.connector
cnx = mysql.connector.connect(user='root', password='22147565Ll^', host='127.0.0.1', database='scraping', port=3306)
df = pd.read_sql('SELECT * FROM job_hunting1', con=cnx)

#%%
def main():
    start = time.time()
    # TODO: Get a list of cities, job_titles for thorough job search on Indeed
    locations = ['Houston, TX', 'Dallas, TX', 'Dallas-Fort Worth, TX', 'San Francisco, CA',
    'New York, NY', 'Philadelphia, PA', 'Pittsburgh, PA', 'Boston, MA', 'Washington, DC', 
    ]

    titles = ['data scientist', 'data analyst', 'machine learning engineer']
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

