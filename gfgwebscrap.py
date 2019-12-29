
##
from requests import get
from bs4 import BeautifulSoup
url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)
#print(response.text[:500])

html_soup =BeautifulSoup(response.text, 'html.parser')
type(html_soup)

movie_containers = html_soup.find_all('div', class_ = 'lister-item-content')
print(type(movie_containers))
print(len(movie_containers))