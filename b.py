from bs4 import BeautifulSoup
import requests


# Luke Skywalker's wookieepedia page url
luke_url = "http://starwars.wikia.com/wiki/Luke_Skywalker"
shuttle_url = "http://starwars.wikia.com/wiki/Lambda-class_T-4a_shuttle"


def request_soup(url):
    """Given a url, requests the page content and returns the soup"""
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup
    

def html_export(filename, soup):
    """Given a filename and a soup, prettifies the soup and writes it to the
    given file
    """
    file = open(filename, "w")
    pretty = soup.prettify().encode('utf-8')
    file.write(pretty)
    file.close


def get_links(soup):
    """Given a soup, extracts all the relevant links from the page content and
    places each one in a dictionary with the page's url and title, and each
    link-dictionary is placed into a list which is returned
    """
    all_links = []
    for tag in soup.select('p a[href]'):
        if "wiki" in tag['href']:
            link = {
                "url": "http://starwars.wikia.com"+tag["href"],
                "title": tag['title']
            }
            all_links.append(link)
    # clean_links represents the original set of links with duplicates removed
    clean_links = [dict(t) for t in set([tuple(d.items()) for d in all_links])]
    return clean_links


def check_character(link):
    """Given a link, requests the page content and checks if the page is a
    character page

    Currently the only way I've found to tell if a page is a character page is
    to check the javascript for the variable 'wgArticleType' with a value of
    "character". Sod's law, some non-characters are still slipping through
    """
    soup = request_soup(link['url'])
    if "wgArticleType=\"character\"," in soup.script.prettify():
        return True
    return False


def get_connections(url):
    """Given a url, checks the content for links, checks if each one is a
    character and prints them if true
    """
    soup = request_soup(url)
    links = get_links(soup)
    for link in links:
        if check_character(link):
            print link['title']


if __name__ == "__main__":
    get_connections(luke_url)
