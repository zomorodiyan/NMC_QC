import unittest
import numpy as np
from BlochClass import Bloch

class TestBlochClass(unittest.TestCase):

  # content of this optional method runs before all of the test in this class
  @classmethod
  def setUpClass(cls):
      pass
  # content of this optional method runs after all of the test in this class
  @classmethod
  def tearDownClass(cls):
      pass
  # content of this optional method runs before each test in this class
  def setUp(self):
      # a sample of how to define variables here:
      # self.object1 = ClassName(initial_variables)
      # you need to use the "self." in tests too
      pass
  # content of this optional method runs after each test in this class
  def tearDown(self):
      pass

  def test_distance(self): # function's name have to start with "test_"

    a = Bloch()
    b = Bloch()
    self.assertRaises(ValueError, a.distance, b)

    a = Bloch([0])
    b = Bloch([0,1])
    self.assertRaises(ValueError, a.distance, b)

    a = Bloch(np.array([0,0]))
    b = Bloch(np.array([3,4]))
    self.assertAlmostEqual(a.distance(b),5)

  def test_values(self):
    # Make sure value errors are raised when necessary
    with self.assertRaises(ValueError):
        a = Bloch(pauli=np.array([0,1]))
    with self.assertRaises(ValueError):
        a = Bloch(pauli=np.array([0.9,0.9]))
    with self.assertRaises(ValueError):
        a = Bloch()
        a.evalpauli()


  def test_types(self):
    # Make sure type error raised when necessary
    self.assertRaises(TypeError, Bloch,np.array([1+1j]))
    self.assertRaises(TypeError, Bloch,np.array([True]))

# list of all asserts:
# assertEqual(a, b)
# assertNotEqual(a, b)
# assertTrue(x)
# assertFalse(x)
# assertIs(a, b)
# assertIsNot(a, b)
# assertIsNone(x)
# assertIsNotNone(x)
# assertIn(a, b)
# assertNotIn(a, b)
# assertIsInstance(a, b)
# assertNotIsInstance(a, b)

# to be able to run unittests using $ python test_file.py
# instead of $ python -m unittest test_file.py
if __name__ == '__main__':
    unittest.main()
