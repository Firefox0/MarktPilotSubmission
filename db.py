import sqlite3

class Db:

    def __init__(self, fileName):
        self.fileName = fileName

    def connect(self):
        if not self.fileName:
            return False
        try:
            self.con = sqlite3.connect(self.fileName)
        except sqlite3.Error as e:
            print(e)
            return False
        self.cur = self.con.cursor()
        return True

    def create(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS products (name text, price text, delivery text, needleSize text, combination text, url text)")
        self.con.commit()

    def insert(self, productDict):
        self.cur.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", (productDict['name'], productDict['price'], productDict['delivery'], productDict['needleSize'], productDict['combination'], productDict['url']))
        self.con.commit()

    def insertProducts(self, productsDict):
        for i in range(len(productsDict)):
            self.insert(productsDict[i])

    def selectAll(self):
        return self.cur.execute("SELECT * FROM products").fetchall()

    def update(self, name, newPrice, newDelivery, newNeedleSize, newCombination, newUrl):
        self.cur.execute(f"UPDATE products "  +
                         f"SET price = '{newPrice}', delivery = '{newDelivery}', " +
                         f"needleSize = '{newNeedleSize}', combination = '{newCombination}', url = '{newUrl}' " +
                         f"WHERE name = '{name}'")
        self.con.commit()

    def delete(self, name):
        self.cur.execute(f"DELETE FROM products WHERE name = '{name}'")
        self.con.commit()

    def close(self):
        self.cur.close()
