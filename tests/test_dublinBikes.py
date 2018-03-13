import unittest

import dublinBikes


class DublinbikesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = dublinBikes.application.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to Dublin Bikes', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
