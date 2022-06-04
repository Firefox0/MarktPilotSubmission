import grequests
import requests
from bs4 import BeautifulSoup
import json
import os

def urlToSoup(url):
    """ Returns a BeautifulSoup object for the url. """
    if not url:
        return False
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def urlsToSoups(urls):
    if not urls or len(urls) == 0:
        return None
    
    responses = asyncRequests(urls)
    return [BeautifulSoup(response.text, "html.parser") for response in responses]

def saveProduct(productDict):
    """ Saves a product in a json file. """
    # Check validity of the argument.
    keys = productDict.keys()
    if len(keys) != 6 or len([e for e in keys if e not in ["name", "price", "delivery", "needleSize", "combination", "url"]]):
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

def saveProducts(productsDict):
    """ Saves multiple products in a json file. """    
    for i in range(len(productsDict)):
        saveProduct(productsDict[i])

def asyncRequests(urls):
    rs = (grequests.get(u) for u in urls)
    return grequests.map(rs)

def searchProduct(companyName, productName, search, getProductInfo, limit=0):
    """ Searches product and parses up to 'limit' product info. """
    urls = search(companyName, productName)
    if not urls or len(urls) == 0:
        return None
    soups = urlsToSoups(urls)
    if limit == 0:
        limit = len(soups)
    productInfo = [getProductInfo(urls[i], soups[i]) for i in range(limit)]
    return productInfo
