import unittest
import common
from selenium import webdriver
import db
import os

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.dbName = "test.db"
        self.db = db.Db(self.dbName)
        self.db.connect()
        self.db.create()

    def testUrlToSoup(self):
        self.assertTrue(common.urlToSoup("https://www.markt-pilot.de/en/home"))
        self.assertFalse(common.urlToSoup(""))

    def testUrlsToSoups(self):
        self.assertTrue(len(common.urlsToSoups(["https://www.markt-pilot.de/en/case-studies", "https://www.markt-pilot.de/en/press"])) == 2)
        self.assertFalse(common.urlsToSoups([]))
    
    def testSaveProduct(self):
        self.assertTrue(common.saveProduct({"name": "", "price": "", "delivery": "", "needleSize": "",
                     "combination": "", "url": ""}))
        self.assertFalse(common.saveProduct({"name": "", "price": "", "delivery": "", "needleSize": "",
                     "combination": ""}))

    def testSearchWollplatz(self):
        driver = self.driver
        driver.get("https://www.wollplatz.de")
        self.assertIn("Wollplatz", driver.title)

    def testSearchDieZauberscheren(self):
        driver = self.driver
        driver.get("https://diezauberscheren.de")
        self.assertIn("Zauberschere", driver.title)

    def tearDown(self):
        self.driver.close()
        self.db.close()

    def testCreateDatabase(self):
        self.db.create()
        self.assertTrue(os.path.exists(self.dbName))

    def testInsertDatabase(self):
        testDict = {"name": "name", "price": "price", "delivery": "delivery", 
                        "needleSize": "needleSize", "combination": "combination", "url": "url"}
        self.db.insert(testDict)
        self.assertTrue(self.db.selectAll()[0] == (testDict["name"], testDict["price"], testDict["delivery"], 
                                                  testDict["needleSize"], testDict["combination"], testDict["url"]))

    def testUpdateDatabase(self):
        self.db.update("name", "test", "test", "test", "test", "test")
        self.assertTrue(self.db.selectAll()[0] == ("name", "test", "test", "test", "test", "test"))

    def testDeleteDatabaseEntry(self):
        self.db.delete("name")
        self.assertTrue(len(self.db.selectAll()) == 0)

if __name__ == "__main__":
    unittest.main()
