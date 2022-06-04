from itertools import product
from urllib import response
import urllib.parse

import common

# br code for each company.
company = {
    "dmc": "23", 
    "drops": "38",
    "stylecraft": "34"
}

def parseSearchQuery(query):
    """ Converts the query to the url search parameter. """
    return f"#sqr:(q[{query}])"

def search(companyName, productName):
    """ Looks for the productName from companyName and returns matches. """
    companyNameLowered = companyName.lower()
    brCode = ""
    try:
        brCode = company[companyNameLowered]
    except KeyError:
        return None
    params = {"br": brCode}
    baseUrl = f"https://www.wollplatz.de/wolle/?"
    productNameLowered = productName.lower()
    finalUrl = baseUrl + urllib.parse.urlencode(params) + parseSearchQuery(productNameLowered)
    soup = common.urlToSoup(finalUrl)
    if not soup:
        return None
    products = soup.find_all("a", {"class": "productlist-imgholder"})
    goodQuery = productName.replace(" ", "-")
    # List comprehension for slightly better performance
    results = [product["href"] for product in products if goodQuery in product["href"]]
    return results

def getProductInfo(url):
    """ Extracts certain info about a product from url. """
    if not url:
        return None
    soup = common.urlToSoup(url)
    if not soup:
        return None
    name = soup.find("h1", {"id": "pageheadertitle"}).text
    price = soup.find("span", {"class": "product-price-amount"}).text
    # Delivery element is dependent on its state.
    # It could either include "green", "orange" or "red".
    # Instead just access the element from the parent to 
    # prevent the need for an iteration.
    deliveryParent = soup.find("div", {"id": "ContentPlaceHolder1_upStockInfoDescription"})
    delivery = deliveryParent.findChild("span").text
    try:
        needleSize = soup.find("td", string="Nadelstärke").nextSibling.text
    except:
        needleSize = "-"
    try:
        combination = soup.find("td", string="Zusammenstellung").nextSibling.text
    except:
        combination = ""
    return {"name": name, "price": price, "delivery": delivery, "needleSize": needleSize, "combination": combination, "url": url}

def searchProduct(companyName, productName, limit=0):
    """ Searches product and parses up to 'limit' product info. """
    url = search(companyName, productName)
    if not url or len(url) == 0:
        return None
    if limit == 0:
        limit = len(url)
    productInfo = [getProductInfo(url[i]) for i in range(limit)]
    return productInfo
