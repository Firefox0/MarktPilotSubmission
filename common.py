import requests
from bs4 import BeautifulSoup

def urlToSoup(url):
    if not url:
        return False
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")
