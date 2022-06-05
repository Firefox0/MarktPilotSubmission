import grequests
import requests
from bs4 import BeautifulSoup
import json
import os

def urlToSoup(url):
    """ Returns a BeautifulSoup object for the url. """
    if not url:
        return None

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
            fp.write(json.dumps({"products": [productDict]}, indent=4))
        return True
        
    text = ""
    with open(fileName, "r+") as fp:
        text = "".join(fp.readlines())
        parsedJson = json.loads(text)
        parsedJson["products"].append(productDict)
        fp.truncate(0)
        fp.seek(0)
        fp.write(json.dumps(parsedJson, indent=4))

    return True

def saveProducts(productsDict):
    """ Saves multiple products in a json file. """    
    for i in range(len(productsDict)):
        saveProduct(productsDict[i])

def asyncRequests(urls):
    rs = (grequests.get(u) for u in urls)
    return grequests.map(rs)
