##
import requests
import bs4
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import time

ap = argparse.ArgumentParser()
ap.add_argument('-URL', '--link', required=False,
                help='a string or a list of strings that specify the links of the job posting')
args = vars(ap.parse_args())
## Import url
URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'
'''https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level
https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level&start=10
https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level&start=20'''
# get the html page using the URL specified above

page = requests.get(URL)

# Specifying the desired format of 'page' using html parser.
# This allows python to read various components of the page,
# rather than treating it as one long string.

soup = BeautifulSoup(page.text, 'html.parser')

# Printing soup in a more structured tree format that makes for easier reading
# print(soup.prettify())
# Loop through tag to get all the job postings in a page
posting_tag = "jobsearch-SerpJobCard unifiedRow row result clickcard"
divs = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
print(len(divs))  # 10 job postings per page


def getJobInfo(divs):
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
            for name in sjcl.find_all('a', attrs={'data-tn-element': 'companyName'}):
                names.append(name.text)
        # Get company locations
        for locs in divs:
            for loc in locs.find_all('span', attrs={'class': 'location accessible-contrast-color-location'}):
                job_locations.append(loc.text)
        # Get the location of the job
    return job_titles, summary_links, names, job_locations


job_titless, summary_linkss, namess, locations = getJobInfo(divs)


##
# Job Summary link
def get_jobdes(summary_links, base_web='https://www.indeed.com'):
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
    for tail in summary_links:
        link = base_web + tail
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        div = soup.find_all('div', attrs={'id': 'jobDescriptionText'})
        summaries.append(div[0].text)
    return summaries


summaries = get_jobdes(summary_linkss)
# import re
# re.sub(r"\[\n\n|\n\n|\n\n\]",' ', test)

##
if __name__ == '__main__':
    start = time.time()
    # Import url
    if args['link']:
        URL = args['link']
    else:
        URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'
    # get the html page using the URL specified above
    try:
        page = requests.get(URL)

        # Specifying the desired format of 'page' using html parser.
        # This allows python to read various components of the page,
        # rather than treating it as one long string.
        soup = BeautifulSoup(page.text, 'html.parser')
        # Get job information from job postings
        # Loop through tag to get all the job postings in a page
        posting_tag = "jobsearch-SerpJobCard unifiedRow row result clickcard"
        divs = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
        print(len(divs))  # 10 job postings per page

        job_titles, summary_links, names, locations = getJobInfo(divs)
        summaries = get_jobdes(summary_links)

        end = time.time()
        # Putting all information into a csv file
        job_postings = {'Company Name': names,
                        'Title': job_titles,
                        'Job Location': locations,
                        'Job Description': summaries}
        Jobs = pd.DataFrame(job_postings)
        print('[INFO] Here\'s the first five job')
        print(Jobs.head())
        input = input('Do you want to continue?')
        input = input.lower()
        if input == 'y' or 'yes':
            Jobs.to_csv('Jobs.csv', header=True, index=None)
        else:
            print('[INFO] exit file without saving ...')
            break
        print(f'[INFO] The execution time is {(end - start) / 60} minutes')
    except Exception as e:
        print(e)
