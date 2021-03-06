from unittest import TestCase
from server import app

class FlaskTests(TestCase):

  def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True

  def test_some_flask_route(self):
      """Some non-database test..."""

      result = self.client.get("/")
      self.assertEqual(result.status_code, 200)
      self.assertIn('',result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()