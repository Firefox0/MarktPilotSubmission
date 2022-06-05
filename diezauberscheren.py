import urllib.parse
import common
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getUrl(driver, product):
    params = {"controller": "search", "s": product}
    driver.get(f"https://diezauberscheren.de/suchen?controller=search&s={urllib.parse.urlencode(params)}")
    try:
        productElem = driver.find_element_by_css_selector(f"a[href^='https://diezauberscheren.de/wolle/{product.lower().replace(' ', '-')}']")
    except:
        return None
    
    return productElem.get_property("href")

def scrape(url, soup):
    name = soup.find("h1", {"itemprop": "name"}).text
    price = soup.find("span", {"itemprop": "price"}).text
    delivery = soup.find("div", {"class": "soy_tiempo_entrega"}).find("span").text
    try:
        needleSize = soup.find("ul", {"class": "data-sheet"}).find_all("span", {"class": "value"})[4].text
    except:
        needleSize = "-"
    try:
        combination = soup.find("section", {"class": "product-description"}).find_all("p")[1].text
    except:
        combination = ""

    return {"name": name, "price": price, "delivery": delivery, "needleSize": needleSize, "combination": combination, "url": url}
