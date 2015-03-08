import unittest
from sklearn.isotonic import IsotonicRegression
import sys

sys.path.append('../../')
from python.c_extensions.python_implementation import proj_PAV
from python.c_extensions.c_extensions import isotonic_regression_c, isotonic_regression_multi_c

import numpy as np

__author__ = 'jeromethai'

class TestIsotonicRegression(unittest.TestCase):

    def setUp(self):
        # The setup code is run before each test
        seed = 237423433
        np.random.seed(seed)


    def test_proj_PAV(self):
        n = 6
        x = np.arange(n)
        y = np.array([4,5,1,6,8,7])
        truth = [3.33333333, 3.33333333, 3.33333333, 6., 7.5, 7.5]
        ir = IsotonicRegression()
        self.assertTrue(np.linalg.norm(ir.fit_transform(x, y) - truth) < 1e-6)
        self.assertTrue(np.linalg.norm(proj_PAV(y) - truth) < 1e-6)


    def test_isotonic_regression_c(self):
        n = 6
        y = np.array([4.,5.,1.,6.,8.,7.])
        w = np.ones(n)
        isotonic_regression_c(y, w, 0, n)
        truth = np.array([3.33333333, 3.33333333, 3.33333333, 6., 7.5, 7.5])
        assert np.linalg.norm(y-truth) < 1e-6


    def test_isotonic_regression_multi_c(self):
        y = np.array([4.,5.,1.,6.,8.,7.])
        blocks = np.array([0, 2, 4])
        isotonic_regression_multi_c(y, np.ones(6), blocks)
        truth = np.array([4., 5., 1., 6., 7.5, 7.5])
        assert np.linalg.norm(y-truth) < 1e-6


if __name__ == '__main__':
    unittest.main()