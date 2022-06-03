import sqlite3

class Db:

    def __init__(self, fileName):
        self.fileName = fileName

    def connect(self):
        if not self.fileName:
            return False
        self.con = sqlite3.connect(self.fileName)
        self.cur = self.con.cursor()
        return True

    def create(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS products (name text, price text, delivery text, needleSize text, combination text)")
        self.con.commit()

    def insert(self, productDict):
        self.cur.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (productDict['name'], productDict['price'], productDict['delivery'], productDict['needleSize'], productDict['combination']))
        self.con.commit()

    def selectAll(self):
        for row in self.cur.execute("SELECT * FROM products"):
            print(row)
