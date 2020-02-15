from bs4 import BeautifulSoup
from flask import Flask, request

import requests
import re

app = Flask(__name__)

@app.route("/scrape")
def scraper():
	# 1. form the url structure
	# 2. make the request
	# 3. check that there are valid anchor tags returned 
	# 4. retrieve the first one
	# 5. extract the title id (CUSA...)

	if 'query' in request.args:
		return search(request.args.get('query'))
	else:
		return "no query provided"

	# 1, we'll ignore for now
	url = 'https://store.playstation.com/en-gb/grid/search-game/1?gameContentType=apps&platform=ps4&sort=name&query=youtube'
	
	# 2, make the request
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	# 3, check valid anchor tags are present
	href = soup.select("a[href*=CUSA]")
	if not href:
		return "couldn't resolve query"
	else: 
		href = href[0]

	title_search = 'CUSA(.*?)[0-9]*'
	
	#link = href.find_all(ref=re.compile(title_search, re.IGNORECASE))
	#link = re.search('/CUSA(.*?)[0-9]*/ig', href)
	title_id = re.search(title_search, href['href'], re.IGNORECASE).group(0)

	print (href.text)
	return 'found: ' + title_id

def search(query):
	BASE_URL = 'https://store.playstation.com'
	SEARCH_URL = '/en-gb/grid/search-game/1?'
	CONTENT_TYPE = 'gameContentType=apps%2Cgames&'
	PLATFORM = 'platform=ps4&'
	SORT_BY = 'sort=name&'

	QUERY = 'query=' + query
	#QUERY = 'query=' + '%20'.join(map(str, queries))
	
	# build url to complete search
	url = BASE_URL + SEARCH_URL + CONTENT_TYPE + PLATFORM + SORT_BY + QUERY
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	# check valid anchor tags are present
	href = soup.select("a[href*=CUSA]")
	if not href:
		return url + "<br><a href=\'"+url+"\' target=\'_blank\'>search</a><br>couldn't resolve query"
	else: 
		href = href[0]

	title_search = 'CUSA(.*?)[0-9]*'
	
	title_id = re.search(title_search, href['href'], re.IGNORECASE).group(0)
	return '<a href=\''+url+'\' target=\'_blank\'>search</a><br>search found: <a href=\''+BASE_URL+href['href']+'\' target=\'_blank\'>' + title_id+'</a>'

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='5001', debug=True)