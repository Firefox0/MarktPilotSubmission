import unittest
import common

class Test(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
