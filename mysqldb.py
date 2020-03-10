# import WebScrape
# import importlib
# importlib.reload(WebScrape)
import sys
from datetime import datetime
from typing import List
import argparse

import mysql.connector
from mysql.connector import errorcode
import pandas as pd

from WebScrape import get_jobdes, getJobInfo, getJobPost

# %% Create Tables
TABLES = {}

TABLES['job_hunting'] = f'''CREATE TABLE IF NOT EXISTS job_hunting
 (company_id SMALLINT UNSIGNED AUTO_INCREMENT,
    job_title VARCHAR(100),
    company_name VARCHAR(100),
    createdDate DATE NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    url VARCHAR(400),
    CONSTRAINT pk_company PRIMARY KEY(company_id)
 );'''
TABLES['job_desc'] = f'''CREATE TABLE IF NOT EXISTS job_desc
(company_id SMALLINT UNSIGNED NOT NULL,
    job_description LONGTEXT,
    createdDate DATE NOT NULL,
    CONSTRAINT pk_company_id PRIMARY KEY (company_id),
    CONSTRAINT fk_comp_desc_id FOREIGN KEY (company_id)
    REFERENCES job_hunting (company_id)
);'''

# DESCRIBE job_desc;

TABLES['job_status'] = f'''CREATE TABLE IF NOT EXISTS job_status(
    company_id SMALLINT UNSIGNED NOT NULL,
    status BOOLEAN DEFAULT 0,
    createdDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_company_id PRIMARY KEY(company_id),
    CONSTRAINT fk_comp_status_id FOREIGN KEY(company_id)
    REFERENCES job_hunting(company_id)
);'''

# %% Create tables into database

DB_NAME = 'scraping'
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='22147565Ll^',
    database='scraping',
)

cursor = cnx.cursor()

def create_database(cursor: mysql.connector.cursor.MySQLCursor):
    try:
        cursor.execute(f'CREATE DATABASE {DB_NAME}')
    except mysql.connector.Error as err:
        print(f'Failed to create database {DB_NAME}')
        sys.exit(1)


def create_table(cursor: mysql.connector.cursor.MySQLCursor):
    try:
        cursor.execute(f'USE {DB_NAME}')
    except mysql.connector.Error as err:
        print(f'Database {DB_NAME} does not exist')
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print(f'Database {DB_NAME} created successfully')
            cnx.database = DB_NAME
        else:
            print(err)
            sys.exit(1)

    for table in TABLES:
        table_description = TABLES[table]
        try:
            print(f'Creating table {table}')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('already exists.')
            else:
                print(err.msg)
        else:
            print('OK')

    cursor.close()
    cnx.close()

def reset_tables(cursor: mysql.connector.cursor.MySQLCursor):
    cursor.execute('DROP TABLE IF EXISTS job_desc;')
    cursor.execute('DROP TABLE IF EXISTS job_status;')
    cursor.execute('DROP TABLE IF EXISTS job_hunting;')
    create_table(cursor=cursor)
    cursor.close()
    cnx.close()

# create_table(cursor=cursor)
reset_tables(cursor=cursor)

# %% Scraping Webs

params = {'q': 'data scientist', 'l': 'Houston, TX',
          'explvl': 'entry_level',
          'jt': 'fulltime', 'start': 0}


def webscrape(params: dict) -> List[List[str]]:
    divs = getJobPost(queries=params)
    # * Get info from job_postings from Indeed.com
    job_titles, summary_links, company_names, locations = getJobInfo(divs=divs)
    # TODO: Get job_descriptions later for NLP project
    summaries = get_jobdes(summary_links=summary_links)
    values_to_insert = [job_titles, summary_links, company_names, locations, summaries]
    return values_to_insert


values_to_insert = webscrape(params=params)
# %% Insert Values

DB_NAME = 'scraping'
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='22147565Ll^',
    database='scraping',
)

def insert_values(values_to_insert: List[List[str]], cnx: mysql.connector.connect = cnx):
    cursor = cnx.cursor()
    cursor.execute('USE scraping')
    job_titles, summary_links, company_names, locations, summaries = values_to_insert
    for job_title, summary_link, company_name, location, job_description in zip(job_titles, summary_links,
                                                                                company_names, locations,
                                                                                summaries):
        if ',' in location:
            city, state = location.split(',')
        else:
            city = location
            state = None
        gen_info = (company_name, city, job_title, datetime.now().date(), state, summary_link)
        statement1 = f'''INSERT INTO job_hunting (company_name, city, job_title, createdDate, state, url)
            VALUES(%s, %s, %s, %s, %s, %s);'''
        cursor.execute(statement1, gen_info)
        id = cursor.lastrowid
        track1 = {'id': id}
        statement2 = f'''INSERT INTO job_status (company_id) 
        VALUES(%(id)s);'''
        statement3 = f'''INSERT INTO job_desc (company_id, job_description, createdDate)
        Values(%(id)s, %(job_desc)s, %(createdDate)s)'''
        cursor.execute(statement2, track1)
        track2 = {'id': id, 'job_desc': job_description, 'createdDate': datetime.now().date()}
        cursor.execute(statement3, track2)
        cnx.commit()
    cursor.close
    cnx.close()


insert_values(values_to_insert=values_to_insert)

# %% Query values as dataframe

cnx = mysql.connector.connect(user='root', password='22147565Ll^', host='127.0.0.1', database='scraping', port=3306)
df = pd.read_sql('SELECT * FROM job_hunting', con=cnx)
df.head()

# %% Save values to a txt file for later test
with open('values_to_insert.txt', 'wb') as file:
    for item in values_to_insert:
        file.write('%s\n' % item)

values_to_insert = []
with open('values_to_insert.txt', 'rb') as file:
    for line in file:
        currentPlace = line[:-1]
        values_to_insert.append(currentPlace)

#%%
if __name__ == '__main__':
    reset_tables(cursor=cursor)
    params = {'q': 'data scientist', 'l': 'Houston, TX',
              'explvl': 'entry_level',
              'jt': 'fulltime', 'start': 0}
    values_to_insert = webscrape(params=params)
    insert_values(values_to_insert=values_to_insert)
