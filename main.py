from email import parser
from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib.parse

# br code for each company.
company = {
    "dmc": "23", 
    "drops": "38",
    "stylecraft": "34"
}

def urlToSoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def parseSearchQuery(query):
    return f"#sqr%3A(q[{query}])"

def search(companyName, productName):
    brCode = company[companyName]
    params = {"br": brCode}
    baseUrl = f"https://www.wollplatz.de/wolle/?"
    finalUrl = baseUrl + urllib.parse.urlencode(params) + parseSearchQuery(productName)
    print(finalUrl)
    soup = urlToSoup(finalUrl)
    products = soup.find_all("a", {"class": "productlist-imgholder"})
    goodQuery = productName.replace(" ", "-")
    # List comprehension for slightly better performance
    results = [product["href"] for product in products if goodQuery in product["href"]]
    print(results)
    return results

def getProductInfo(url):
    soup = urlToSoup(url)
    price = soup.find("span", {"class": "product-price-amount"})
    print(price.text)
    # Delivery element is dependent on its state.
    # It could either include "green", "orange" or "red".
    # Instead just access the element from the parent to 
    # prevent the need for an iteration.
    deliveryParent = soup.find("div", {"id": "ContentPlaceHolder1_upStockInfoDescription"})
    delivery = deliveryParent.findChild("span")
    print(delivery.text)
    needleSize = soup.find("td", string="Nadelstärke").nextSibling.text
    print(needleSize)

url = search("dmc", "natura xl")[0]
getProductInfo(url)
input("")
