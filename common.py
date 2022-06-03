import requests
from bs4 import BeautifulSoup

def urlToSoup(url):
    """ Returns a BeautifulSoup object for the url. """
    if not url:
        return False
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")
