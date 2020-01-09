# URL_more = URL + '&start={}'.format(iter * jobs_per_page)
URL_more = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level&start=20'
page = requests.get(URL_more)

# Specifying the desired format of 'page' using html parser.
# This allows python to read various components of the page,
# rather than treating it as one long string.
print(f'[INFO] Getting information from the provided URL starting at {iter * jobs_per_page} job posting...')
soup = BeautifulSoup(page.text, 'html.parser')
# Get job information from job postings
# Loop through tag to get all the job postings in a page
posting_tag = "jobsearch-SerpJobCard unifiedRow row result clickcard"
divs = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
print('[INFO] The number of job postings on this page is:')
print(len(divs))  # 10 job postings per page
job_titles, summary_links, names, locations = getJobInfo(divs)
print(len(job_titles), len(summary_links), len(names), len(locations))
summaries = get_jobdes(summary_links)
print(len(summaries))
# print('[INFO] all information scrapped, preparing to write to a csv file ...')
# Putting all information into a csv file
job_postings = {'Company Name': names,
                'Title': job_titles,
                'Job Location': locations,
                'Job Description': summaries}
Jobss = pd.DataFrame(job_postings)
Jobs = pd.concat([Jobs, Jobss], ignore_index=True)
iter += 1
