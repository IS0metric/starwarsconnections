from bs4 import BeautifulSoup
import requests

luke_url = "http://starwars.wikia.com/wiki/Luke_Skywalker"
page = requests.get(luke_url)

a = page.content

soup = BeautifulSoup(a, 'html.parser')

urls = []

for link in soup.find_all('a'):
    url = link.get('href')
    if url is not None and 'wiki' in url:
        urls.append(url)

file = open("o.html", "w")


pretty = soup.prettify().encode('utf-8')

all_links = [tag['title'] for tag in soup.select('p a[title]')]

#for para in soup.find_all('p').get('a'):
#    print para

print all_links

file.write(pretty)
file.close
