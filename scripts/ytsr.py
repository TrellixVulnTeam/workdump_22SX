#! python3

import urllib.request
import sys
from bs4 import BeautifulSoup

textToSearch = sys.argv[1] if len(sys.argv) > 1 else input()
query = urllib.parse.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
    text = vid.find('span').text if vid.find('span') is not None \
        else vid.text.encode('ascii', 'ignore').decode('ascii', 'ignore')
    print(f"https://www.youtube.com{vid['href']}\t{text}")
