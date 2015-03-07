import unittest
import time

__author__ = 'jeromethai'

import sys
sys.path.append('../../python/isotonic_regression/')
from isotonic_regression import proj_PAV
from isotonic_regression_c import isotonic_regression_c, isotonic_regression_multi_c
import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.utils import check_random_state

class TestStressIsotonicRegression(unittest.TestCase):
    
    def setUp(self):
        # The setup code is run before each test
        seed = 237423433
        np.random.seed(seed)


    def test_isotonic_regression(self):
        times = []
        for n in [int(1e3), int(1e4)]:
            x = np.arange(n)
            rs = check_random_state(0)
            y = rs.randint(-50, 50, size=(n,)) + 50. * np.log(1 + np.arange(n))
            ir = IsotonicRegression()
            start_time = time.time()
            y1 = ir.fit_transform(x, y)
            times.append(time.time() - start_time)
        print 'test isotonic_regression'
        print times


    def test_proj_PAV(self):
        times = []
        for n in [int(1e3), int(1e4)]:
            rs = check_random_state(0)
            y = rs.randint(-50, 50, size=(n,)) + 50. * np.log(1 + np.arange(n))
            start_time = time.time()
            proj_PAV(y)
            times.append(time.time() - start_time)
        print 'test proj_PAV'
        print times


    def test_isotonic_regression_c(self):
        times = []
        for n in [int(1e3), int(1e4), int(1e5), int(1e6)]:
            rs = check_random_state(0)
            y = rs.randint(-50, 50, size=(n,)) + 50. * np.log(1 + np.arange(n))
            w = np.ones(n)
            start_time = time.time()
            isotonic_regression_c(y, w, 0, n)
            times.append(time.time() - start_time)
        print 'test isotonic_regression_c'
        print times


    def test_isotonic_regression_multi_c(self):
        n = int(1e6)
        w = np.ones(n)
        times = []
        for num_blocks in [int(1e1), int(1e2), int(1e3), int(1e4)]:
            rs = check_random_state(0)
            y = rs.randint(-50, 50, size=(n,)) + 50. * np.log(1 + np.arange(n))
            blocks = np.sort(np.random.choice(n, num_blocks, replace=False))
            start_time = time.time()
            isotonic_regression_multi_c(y, w, blocks)
            times.append(time.time() - start_time)
        print 'test isotonic_regression_multi_c'
        print times






if __name__ == '__main__':
    unittest.main()