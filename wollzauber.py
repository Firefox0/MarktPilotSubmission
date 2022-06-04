import re
import common
from bs4 import BeautifulSoup

# s code for each company.
company = {
    "dmc": "50",
    "go handmade": "63"
}

def search(companyName, productName):
    """ Looks for the productName from companyName and returns matches. """
    companyNameLowered = companyName.lower()
    sCode = ""
    try:
        sCode = company[companyNameLowered]
    except KeyError:
        return None
    baseUrl = f"https://wollzauber.com/wolle/?p=1&o=1&n=50&s={sCode}"
    productNameLowered = productName.lower()
    finalUrl = baseUrl
    soup = common.urlToSoup(finalUrl)
    if not soup:
        return None
    products = soup.find_all("a", {"class": "product--title"})
    # List comprehension for slightly better performance
    results = [product["href"] for product in products if productNameLowered in product.text.lower()]
    return results

def getProductInfo(url, soup):
    """ Extracts certain info about a product from url. """
    if not url or not soup:
        return None
    name = soup.find("h1", {"class": "product--title"}).text
    price = soup.find("span", {"class": "price--content"}).text.strip().split("€")[0][:-1]
    delivery = soup.find("i", {"class": "delivery--status-icon"}).nextSibling
    table = soup.find("div", {"class": "product--description"})
    try:
        needleSize = table.find("li", string=re.compile("^Nadelstärke")).text.split(" ", 1)[1]
    except:
        needleSize = "-"
    try:
        combination = table.find("li", string=re.compile("^Qualität")).text.split(" ", 1)[1]
    except:
        combination = "-"
    return {"name": name, "price": price, "delivery": delivery, "needleSize": needleSize, "combination": combination, "url": url}
