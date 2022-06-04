import common
import wollplatz
import wollzauber
import db

if __name__ == "__main__":
    products = [("go handmade", "couture"), ("dmc", "mouline"), ("drops", "safran"), ("drops", "baby merino"), ("hahn", "alpacca speciale"), ("stylecraft", "special")]
    modules = [wollplatz, wollzauber]
    db = db.Db("database.db")
    db.connect()
    db.create()
    for companyName, productName in products:
        for module in modules:
            productInfo = common.searchProduct(companyName, productName, module.search, module.getProductInfo)
            print(productInfo)
            if not productInfo:
                continue
            common.saveProducts(productInfo)
            db.insertProducts(productInfo)

    db.selectAll()
