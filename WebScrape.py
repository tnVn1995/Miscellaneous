from bs4 import BeautifulSoup
from typing import List, Tuple
import requests

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


def getJobPost(URL: str = 'http://www.indeed.com/jobs?', queries: dict = None) -> BeautifulSoup:
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

#%%
if __name__ == '__main__':
    params = {'q': 'data scientist', 'l': 'Houston, TX',
              'explvl': 'entry_level',
              'jt': 'fulltime', 'start': 0}
    divs = getJobPost(queries=params)
    print(divs)

#%%
# import numpy as np
#
# print(73 - 2*15/np.sqrt(5))
# print(73 + 2*15/np.sqrt(5))
#%%