import unittest
import common
from selenium import webdriver

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

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

if __name__ == "__main__":
    unittest.main()
