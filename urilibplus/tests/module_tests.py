""" 
`module_tests`

Holds tests that relate to the main module.
"""

import unittest
from urilibplus import URI, URIPath, URIQuery

class TestURIExample(unittest.TestCase):
    """
    `TestURIExample`

    Test cases for the `URI` object with a given example.
    """

    URI_EXAMPLE = "http://www.example.com/index.html"

    def test_creation(self):
        """
        `test_creation`
        
        A simple test ensuring that the creation of a `URI` object
        from the given example does not throw an error.
        """
        try:
            _ = URI(self.URI_EXAMPLE)
        except: #pylint:disable=bare-except
            self.fail()

    def test_scheme(self):
        """
        `test_scheme`
        
        Tests that `URI.scheme` returns the exact scheme from the given example.
        """
        self.assertEqual(URI(self.URI_EXAMPLE).scheme, "http")

    def test_host(self):
        """
        `test_host`
        
        Tests that `URI.host` returns the exact host from the given example.
        """
        self.assertEqual(URI(self.URI_EXAMPLE).host, "www.example.com")

    def test_path(self):
        """
        `test_path`
        
        Tests that `URI.path` returns the exact path from the given example.
        """
        self.assertEqual(URI(self.URI_EXAMPLE).path, URIPath("index.html"))

class TestURIPathExample(unittest.TestCase):
    """
    `TestURIPathExample`

    Test cases for the `URIPath` object with a given example.
    """
    EXAMPLE_PATH = "/3/library/urllib.parse.html"

    def test_creation(self):
        """
        `test_creation`
        
        A simple test ensuring that the creation of a `URIPath` object
        from the given example does not throw an error.
        """
        try:
            _ = URIPath(self.EXAMPLE_PATH)
        except: #pylint:disable=bare-except
            self.fail()

    def test_iter(self):
        """
        `test_iter`
        
        Tests that `URIPath` iterates as expected from the given example.
        """
        path_tup = tuple(URIPath(self.EXAMPLE_PATH))
        self.assertTupleEqual(path_tup, ("/", "3", "library", "urllib.parse.html"))

class TestURIQueryExample(unittest.TestCase):
    """
    `TestURIQueryExample`

    Test cases for the `URIQuery` object with a given example.
    """
    QUERY_EXAMPLE = "field1=value1&field2=value2&field3=value3"

    def test_creation(self):
        """
        `test_creation`
        
        A simple test ensuring that the creation of a `URIQuery` object
        from the given example does not throw an error.
        """
        try:
            _ = URIQuery(self.QUERY_EXAMPLE)
        except: #pylint:disable=bare-except
            self.fail()

    def test_encode(self):
        """
        `test_encode`
        
        Tests that `URIQuery` encodes as expected from the given example.
        """
        self.assertEqual(URIQuery(self.QUERY_EXAMPLE).encode(), self.QUERY_EXAMPLE)

    def test_len(self):
        """
        `test_len`
        
        Tests that the lengths of `URIQuery` acts as expected from the given example.
        """
        self.assertEqual(len(URIQuery(self.QUERY_EXAMPLE)), 3)

    def test_get_values(self):
        """
        `test_get_values`
        
        Tests that `URIQuery` gets items as expected from the given example.
        """
        self.assertEqual(tuple(URIQuery(self.QUERY_EXAMPLE).getvalues("field1")), ("value1",))
        self.assertEqual(tuple(URIQuery(self.QUERY_EXAMPLE).getvalues("field2")), ("value2",))
        self.assertEqual(tuple(URIQuery(self.QUERY_EXAMPLE).getvalues("field3")), ("value3",))

    def test_append(self):
        """
        `test_append`
        
        Tests that `URIQuery` appends items as expected from the given example.
        """
        obj = URIQuery(self.QUERY_EXAMPLE)
        obj.append("field4=value4")
        self.assertEqual(tuple(obj.getvalues("field4")), ("value4",))

    def test_set_values(self):
        """
        `test_append`
        
        Tests that `URIQuery` sets items as expected from the given example.
        """
        obj = URIQuery(self.QUERY_EXAMPLE)
        obj.setvalues("field1", "coolervalue1")
        self.assertEqual(tuple(obj.getvalues("field1")), ("coolervalue1",))

if __name__ == '__main__':
    unittest.main()
