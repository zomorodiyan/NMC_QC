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

  def test_dim(self):
      a=Bloch(feature=np.array([1,2]))
      self.assertAlmostEqual(a.dim,2)

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

  def test_evalpauli(self):
    # Make sure pauli components are calculated correctly
    a=Bloch(feature=[1,1]); a.evalpauli() # 2D
    np.testing.assert_array_almost_equal(a.pauli, [2/3,2/3,1/3])
    a=Bloch(feature=[1,2,3]); a.evalpauli()  #3D
    np.testing.assert_array_almost_equal(a.pauli,[2/15,4/15,6/15,13/15])
    a=Bloch(feature=[1,0,0,1]); a.evalpauli()  #4D
    np.testing.assert_array_almost_equal(a.pauli,[2/3,0/3,0/3,2/3,1/3])

  def test_evalfeature(self):
    # Make sure features are calculated correctly for n+1 dimensional pauli co.
    a=Bloch(pauli=[2/3,2/3,1/3]); a.evalfeature() # 2D
    np.testing.assert_array_almost_equal(a.feature, [1,1])
    a=Bloch(pauli=[2/15,4/15,6/15,13/15]); a.evalfeature()  #3D
    np.testing.assert_array_almost_equal(a.feature, [1,2,3])
    a=Bloch(pauli=[2/3,0/3,0/3,2/3,1/3]); a.evalfeature()  #4D
    np.testing.assert_array_almost_equal(a.feature, [1,0,0,1])

  def test_paulimatrix(self):
    a=Bloch(); #undefined dim
    self.assertRaises(ValueError, a.pauli_matrix, n=0)
    a=Bloch(); a.dim=2 #invalid n
    self.assertRaises(ValueError, a.pauli_matrix, n=4)
    self.assertRaises(ValueError, a.pauli_matrix, n=-4)
    a=Bloch(); a.dim=2 # 2D
    np.testing.assert_array_almost_equal(a.pauli_matrix(0),[[0,1],[1,0]])
    np.testing.assert_array_almost_equal(a.pauli_matrix(1),[[0,-1j],[1j,0]])
    np.testing.assert_array_almost_equal(a.pauli_matrix(2),[[1,0],[0,-1]])
    a=Bloch(); a.dim=3 # 3D
    np.testing.assert_array_almost_equal(a.pauli_matrix(0)\
            ,[[0,1,0],[1,0,0],[0,0,0]])
    np.testing.assert_array_almost_equal(a.pauli_matrix(1)\
            ,[[0,0,1],[0,0,0],[1,0,0]])
    np.testing.assert_array_almost_equal(a.pauli_matrix(6)\
            ,[[1,0,0],[0,-1,0],[0,0,0]])
    a=Bloch(); a.dim=4 # 4D
    np.testing.assert_array_almost_equal(a.pauli_matrix(0)\
            ,[[0,1,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]])
    np.testing.assert_array_almost_equal(a.pauli_matrix(6)\
            ,[[0,-1j,0,0],[1j,0,0,0],[0,0,0,0],[0,0,0,0]])
    np.testing.assert_array_almost_equal(a.pauli_matrix(14)\
        ,[[1/6**0.5,0,0,0],[0,1/6**0.5,0,0],[0,0,1/6**0.5,0],[0,0,0,-3/6**0.5]])

  def test_densitymatrix(self):
    with self.assertRaises(ValueError):
        a = Bloch() #undefined pauli and feature
        a.evaldensity()
    a = Bloch(feature=[1,1]); a.evaldensity() # 2D
    np.testing.assert_array_almost_equal(a.density\
        ,[[5/6,2/3*(1-1j)],[2/3*(1+1j),1/6]])

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
