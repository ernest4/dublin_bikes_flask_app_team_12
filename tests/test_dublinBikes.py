import unittest
from dublinBikes.run import application


class DublinbikesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = application.test_client()

    def test_index(self):
        rv = self.app.get('/')
        contents = ""
        with open("dublinBikes/templates/index.html", "r") as file:
            contents += file.readline()
            
        self.assertIn(contents, rv.data.decode())


if __name__ == '__main__':
    unittest.main()
