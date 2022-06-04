import common
import wollplatz
import wollzauber
import db

if __name__ == "__main__":
    products = [("go handmade", "couture"), ("dmc", "mouline"), ("drops", "safran"), ("drops", "baby merino"), ("hahn", "alpacca speciale"), ("stylecraft", "special")]
    funcs = [wollplatz.searchProduct, wollzauber.searchProduct]
    db = db.Db("database.db")
    db.connect()
    db.create()
    for companyName, productName in products:
        for func in funcs:
            productInfo = func(companyName, productName)
            if not productInfo:
                continue
            common.saveProducts(productInfo)
            db.insertProducts(productInfo)

    db.selectAll()
