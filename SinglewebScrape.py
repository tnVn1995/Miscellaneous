##
import requests
from bs4 import BeautifulSoup
from typing import TypeVar, Any, List, Callable, Dict, Generic
import pandas as pd

Res = TypeVar('bs4tag', List[str], List)


class Content:
    def __init__(self, name:str, url: str, jobInfo: List[Dict[str, str]]):
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
    def getPage(self, url: str) -> Res:
        """Request content from the specified url and return a bs4 tag"""
        print('[INFO] Getting information from the provided URl...')
        try:
            res = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
        return BeautifulSoup(res.text, 'html.parser')

    def getTag(self, bs4tag: Res, tag: str, attribute: Dict[str, str]) -> List[str]:
        """Find the content from the tags given with specified attributes and return a bs4tag"""
        return bs4tag.find_all(tag, attrs=attribute)

class Indeed:
    def __init__(self, bs4tag: Res):
        self.bs4tag = bs4tag
        self.jobInfo_ = []

    def getInfo(self):
        """Getting the requested information from a bs4 tag"""
        print('[INFO] Getting job postings info ...')
        crawler = Crawler()
        for idx, div in enumerate(self.bs4tag):
            try:
                temp_info = {}
                temp_info['title'] = crawler.getTag(bs4tag=div, tag='a', attribute={'data-tn-element': 'jobTitle'})[0].text
                temp_info['summary_links'] = crawler.getTag(bs4tag=div, tag='a', attribute={'data-tn-element': 'jobTitle'})[0]['href']
                temp_info['company name'] = crawler.getTag(bs4tag=div, tag='span', attribute={'class': 'company'})[0].text
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
    divs = Crawler.getTag(soup, tag = 'dib', attribute={'data-tn-component': 'organicJob'})
    indeed = Indeed(divs)
    jobInfo = indeed.getInfo()
    # Save info scraped into a csv file
    content = Content('Indeed',URL, jobInfo)
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
    crawler.getTag(bs4tag=div, tag='span', attribute={'class': 'location accessible-contrast-color-location'})[0].text

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

##
        for idx, div in enumerate(indeed.bs4tag):
            try:
                temp_info = {}
                temp_info['title'] = crawler.getTag(bs4tag=div tag='a', attribute={'data-tn-element': 'jobTitle'})[0].text
                temp_info['summary_links'] = crawler.getTag(bs4tag=div, tag='a', attribute={'data-tn-element': 'jobTitle'})[0]['href']
                temp_info['company name'] = crawler.getTag(bs4tag=divs[8], tag='span', attribute={'class': 'company'})[0].text
                temp_info['location'] = crawler.getTag(bs4tag=div, tag='span', attribute={'class': 'location '
                                                                                                        'accessible'
                                                                                                        '-contrast-color'
                                                                                                        '-location'})[0].text
                indeed.jobInfo_.append(temp_info)
            except IndexError:
                print(idx)
##
div1 =  <div class="jobsearch-SerpJobCard unifiedRow row result" data-jk="02d9b8a455253f6e" data-tn-component="organicJob" id="p_02d9b8a455253f6e">
<div class="title">
<a class="jobtitle turnstileLink" data-tn-element="jobTitle" href="/rc/clk?jk=02d9b8a455253f6e&amp;fccid=9ee66ada40315e6d&amp;vjs=3" id="jl_02d9b8a455253f6e" onclick="setRefineByCookie(['explvl']); return rclk(this,jobmap[8],true,0);" onmousedown="return rclk(this,jobmap[8],0);" rel="noopener nofollow" target="_blank" title="Data Scientist">
Data Scientist</a>
</div>
<div class="sjcl">
<div class="recJobLoc" data-rc-loc="San Antonio, TX" id="recJobLoc_02d9b8a455253f6e" style="display: none"></div>
<span class="location accessible-contrast-color-location">San Antonio, TX</span>
</div>
<div class="summary">
<ul style="list-style-type:circle;margin-top: 0px;margin-bottom: 0px;padding-left:20px;"> <li>The objective of this fellowship is to participate in the collection and analysis of MHS health data, using accepted Data Science Techniques in population…</li></ul></div>
<div class="jobsearch-SerpJobCard-footer">
<div class="jobsearch-SerpJobCard-footerActions">
<div class="result-link-bar-container">
<div class="result-link-bar"><span class="result-link-source">Oak Ridge Associated Universities</span><span class="result-link-bar-separator">·</span><span class="date">30+ days ago</span><span class="tt_set" id="tt_set_8"><span class="result-link-bar-separator">·</span><a class="sl resultLink save-job-link" href="#" id="sj_02d9b8a455253f6e" onclick="changeJobState('02d9b8a455253f6e', 'save', 'linkbar', false, ''); return false;" title="Save this job to my.indeed">Save job</a><span class="result-link-bar-separator">·</span><a class="sl resultLink more-link" href="#" id="tog_8" onclick="toggleMoreLinks('02d9b8a455253f6e'); return false;">more...</a></span><div class="edit_note_content" id="editsaved2_02d9b8a455253f6e" style="display:none;"></div><script>if (!window['result_02d9b8a455253f6e']) {window['result_02d9b8a455253f6e'] = {};}window['result_02d9b8a455253f6e']['showSource'] = true; window['result_02d9b8a455253f6e']['source'] = "Oak Ridge Associated Universities"; window['result_02d9b8a455253f6e']['loggedIn'] = false; window['result_02d9b8a455253f6e']['showMyJobsLinks'] = false;window['result_02d9b8a455253f6e']['undoAction'] = "unsave";window['result_02d9b8a455253f6e']['relativeJobAge'] = "30+ days ago";window['result_02d9b8a455253f6e']['jobKey'] = "02d9b8a455253f6e"; window['result_02d9b8a455253f6e']['myIndeedAvailable'] = true; window['result_02d9b8a455253f6e']['showMoreActionsLink'] = window['result_02d9b8a455253f6e']['showMoreActionsLink'] || true; window['result_02d9b8a455253f6e']['resultNumber'] = 8; window['result_02d9b8a455253f6e']['jobStateChangedToSaved'] = false; window['result_02d9b8a455253f6e']['searchState'] = "q=Data Scientist&amp;l=Texas&amp;start=10"; window['result_02d9b8a455253f6e']['basicPermaLink'] = "https://www.indeed.com"; window['result_02d9b8a455253f6e']['saveJobFailed'] = false; window['result_02d9b8a455253f6e']['removeJobFailed'] = false; window['result_02d9b8a455253f6e']['requestPending'] = false; window['result_02d9b8a455253f6e']['notesEnabled'] = true; window['result_02d9b8a455253f6e']['currentPage'] = "serp"; window['result_02d9b8a455253f6e']['sponsored'] = false;window['result_02d9b8a455253f6e']['reportJobButtonEnabled'] = false; window['result_02d9b8a455253f6e']['showMyJobsHired'] = false; window['result_02d9b8a455253f6e']['showSaveForSponsored'] = false; window['result_02d9b8a455253f6e']['showJobAge'] = true; window['result_02d9b8a455253f6e']['showHolisticCard'] = true; window['result_02d9b8a455253f6e']['showDislike'] = false; window['result_02d9b8a455253f6e']['showKebab'] = false;</script></div></div>
</div>
</div>
<div class="tab-container">
<div class="more-links-container result-tab" id="tt_display_8" style="display:none;"><a class="close-link closeLink" href="#" onclick="toggleMoreLinks('02d9b8a455253f6e'); return false;" title="Close"></a><div class="more_actions" id="more_8"><ul><li><span class="mat">View all <a href="/l-San-Antonio,-TX-jobs.html">San Antonio, TX jobs</a></span></li><li><span class="mat">Salary Search: <a href="/salaries/data-scientist-Salaries,-San-Antonio-TX" onmousedown="this.href = appendParamsOnce(this.href, '?campaignid=serp-more&amp;fromjk=02d9b8a455253f6e&amp;from=serp-more');">Data Scientist salaries in San Antonio, TX</a></span></li><li><span class="mat">Related forums: <a href="/forum/cmp/Orau__orise.html">ORAU/ORISE</a> - <a href="/forum/loc/SAN-Antonio-Texas.html">SAN Antonio, Texas</a></span></li></ul></div></div><div class="dya-container result-tab"></div>
<div class="tellafriend-container result-tab email_job_content"></div>
<div class="sign-in-container result-tab"></div>
<div class="notes-container result-tab"></div>
</div>
</div>