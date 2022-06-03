import wollplatz
import db

if __name__ == "__main__":
    products = [("dmc", "natura xl"), ("drops", "baby"), ("drops", "andes")]
    db = db.Db("database.db")
    db.connect()
    db.create()
    for companyName, productName in products:
        url = wollplatz.search(companyName, productName)
        if len(url) == 0:
            continue
        productInfo = wollplatz.getProductInfo(url[0])
        print(productInfo)

        db.insert(productInfo)

    db.selectAll()
