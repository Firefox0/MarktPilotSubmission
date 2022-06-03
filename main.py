from email import parser
from itertools import product
from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os

# br code for each company.
company = {
    "dmc": "23", 
    "drops": "38",
    "stylecraft": "34"
}

def urlToSoup(url):
    if not url:
        return False
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def parseSearchQuery(query):
    return f"#sqr%3A(q[{query}])"

def search(companyName, productName):
    brCode = company[companyName]
    params = {"br": brCode}
    baseUrl = f"https://www.wollplatz.de/wolle/?"
    finalUrl = baseUrl + urllib.parse.urlencode(params) + parseSearchQuery(productName)
    soup = urlToSoup(finalUrl)
    if not soup:
        return False
    products = soup.find_all("a", {"class": "productlist-imgholder"})
    print(products)
    goodQuery = productName.replace(" ", "-")
    # List comprehension for slightly better performance
    results = [product["href"] for product in products if goodQuery in product["href"]]
    return results

def getProductInfo(url):
    if not url:
        return False
    soup = urlToSoup(url)
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

def saveProduct(productDict):
    # Check validity of the argument.
    keys = productDict.keys()
    if len(keys) != 5 or len([e for e in keys if e not in ["name", "price", "delivery", "needleSize", "combination"]]):
        return False
    fileName = "products.json"
    if not os.path.exists(fileName):
        with open(fileName, "w") as fp:
            fp.write(json.dumps({"products": [productDict]}))
        return

    text = ""
    with open(fileName, "r") as fp:
        text = "".join(fp.readlines())

    parsedJson = json.loads(text)
    parsedJson["products"].append(productDict)

    with open(fileName, "w") as fp:
        fp.write(json.dumps(parsedJson))

    return True
    
if __name__ == "__main__":
    url = search("drops", "baby")[0]
    print(url)
    info = getProductInfo(url)
    print(info)
    saveProduct(info)
    input("")
