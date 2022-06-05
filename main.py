import common
import wollplatz
import diezauberscheren
import db
from selenium import webdriver

if __name__ == "__main__":
    products = ["DMC Natura XL", "Drops Safran", "Drops Baby Merino Mix", "Hahn Alpacca Speciale", "Stylecraft Special double knit"]
    modules = [wollplatz, diezauberscheren]
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    db = db.Db("database.db")
    db.connect()
    db.create()
    for module in modules:
        urls = []
        for product in products:
            print(f"Looking for: {product}")
            tmp = module.getUrl(driver, product)
            if not tmp:
                continue
            urls.append(tmp)
        
        soups = common.urlsToSoups(urls)
        productInfo = [module.scrape(urls[i], soups[i]) for i in range(len(urls))]
        common.saveProducts(productInfo)
        db.insertProducts(productInfo)

    driver.close()
    db.selectAll()
