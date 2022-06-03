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
    return f"#sqr%3A(q[{query}])"

def search(companyName, productName):
    """ Looks for the productName from companyName and returns matches. """
    brCode = company[companyName]
    params = {"br": brCode}
    baseUrl = f"https://www.wollplatz.de/wolle/?"
    finalUrl = baseUrl + urllib.parse.urlencode(params) + parseSearchQuery(productName)
    soup = common.urlToSoup(finalUrl)
    if not soup:
        return False
    products = soup.find_all("a", {"class": "productlist-imgholder"})
    goodQuery = productName.replace(" ", "-")
    # List comprehension for slightly better performance
    results = [product["href"] for product in products if goodQuery in product["href"]]
    return results

def getProductInfo(url):
    """ Extracts certain info about a product from url. """
    if not url:
        return False
    soup = common.urlToSoup(url)
    if not soup:
        return False
    name = soup.find("h1", {"id": "pageheadertitle"}).text
    price = soup.find("span", {"class": "product-price-amount"}).text
    # Delivery element is dependent on its state.
    # It could either include "green", "orange" or "red".
    # Instead just access the element from the parent to 
    # prevent the need for an iteration.
    deliveryParent = soup.find("div", {"id": "ContentPlaceHolder1_upStockInfoDescription"})
    delivery = deliveryParent.findChild("span").text
    needleSize = soup.find("td", string="Nadelstärke").nextSibling.text
    combination = soup.find("td", string="Zusammenstellung").nextSibling.text
    return {"name": name, "price": price, "delivery": delivery, "needleSize": needleSize, "combination": combination}
