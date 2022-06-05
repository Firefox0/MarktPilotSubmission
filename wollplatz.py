def getUrl(driver, product):
    driver.get(f"https://www.wollplatz.de/wolle?#sqr:(q[{product}])")
    driver.refresh()
    try:
        productElem = driver.find_element_by_css_selector(f"a[title='{product}']")
    except:
        return None

    return productElem.get_property("href")

def scrape(url, soup):
    name = soup.find("h1", {"id": "pageheadertitle"}).text
    price = soup.find("span", {"class": "product-price-amount"}).text
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
