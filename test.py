import unittest
import wollplatz
import common

class Test(unittest.TestCase):
    def testParseSearchQuery(self):
        self.assertEqual(wollplatz.parseSearchQuery("test"), "#sqr%3A(q[test])")

    def testSearch(self):
        url = wollplatz.search("dmc", "natura xl")[0]
        self.assertDictEqual(wollplatz.getProductInfo(url), {'name': 'DMC Natura XL 02 Black', 'price': '8,46', 'delivery': 'Lieferbar', 'needleSize': '8 mm', 'combination': '100% Baumwolle'})

    def testUrlToSoup(self):
        self.assertFalse(common.urlToSoup(""))
        self.assertTrue(common.urlToSoup("https://www.markt-pilot.de/en/career"))


if __name__ == "__main__":
    unittest.main()
