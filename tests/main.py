import unittest
from rocamgo.cte import BLACK


class TestStringMethods(unittest.TestCase):

  def test_cte(self):
      self.assertEqual(BLACK, 1)

if __name__ == '__main__':
    unittest.main()
