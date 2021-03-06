import unittest
import sys

sys.path.append('../../')
from python.c_extensions.c_extensions import quad_obj_c, line_search_quad_obj_c, x2z_c, z2x_c
from python.bsls_utils import almost_equal
from cvxopt import matrix

import numpy as np

__author__ = 'jeromethai'

class TestCythonExtensions(unittest.TestCase):

    def setUp(self):
        seed = 237423433
        np.random.seed(seed)


    def test_quad_obj(self):
        for n in range(2,10):
            x = 2*np.random.rand(n) - 1
            Q = 2*np.random.rand(n,n) - 1
            Q_flat = Q.flatten()
            c = 2*np.random.rand(n) - 1
            x2, Q2, c2 = matrix(x), matrix(Q), matrix(c)
            g = np.zeros(n)
            f = quad_obj_c(x, Q_flat, c, g)
            f2 = (.5 * x2.T * Q2 * x2 + c2.T * x2)[0]
            g2 = Q2 * x2 + c2
            assert abs(f2-f) < 1e-6
            for i in range(n): assert abs(g[i]-g2[i]) < 1e-6


    def helper(self, x, f, g, x_new, f_new, g_new, x_true, f_true, g_true, t_true, Q, c):
        # x_new, f_new, g_new, t = line_search_quad_obj(x, f, g, x_new, f_new, g_new, Q, c)
        f_new = line_search_quad_obj_c(x, f, g, x_new, f_new, g_new, Q, c)
        assert np.linalg.norm(x_new - x_true) < 1e-8
        assert abs(f_new - f_true) < 1e-8
        assert np.linalg.norm(g_new - g_true) < 1e-6
        #assert abs(t - t_true) < 1e-8


    def test_line_search(self):
        Q = 2 * np.array([[2, .5], [.5, 1]])
        Q_flat = Q.flatten()
        c = np.array([1.0, 1.0])
        # test 1
        x, f, g = np.array([0.5, 0.5]), 2., np.array([3.5, 2.5])
        x_new, f_new, g_new = np.array([0., 1.]), 2., np.array([2., 3.])
        x_true, f_true, g_true = np.array([0.25, 0.75]), 1.875, np.array([2.75, 2.75])
        t_true = 0.5
        self.helper(x, f, g, x_new, f_new, g_new, x_true, f_true, g_true, t_true, Q_flat, c)

        # test 2
        x_new, f_new, g_new = np.array([0., 1.]), 2., np.array([2., 3.])
        self.helper(x_true, f_true, g_true, x_new, f_new, g_new, x_true, f_true, g_true, 0.0, Q_flat, c)

        # test 3
        x, f, g = np.array([0.26, 0.74]), 1.8752, np.array([2.78, 2.74])
        x_new, f_new, g_new = np.array([0., 1.]), 2., np.array([2., 3.])
        x_true, f_true, g_true = np.array([0.2559375, 0.7440625]), 1.87507050781, np.array([2.7678125, 2.7440625])
        t_true = 0.125
        self.helper(x, f, g, x_new, f_new, g_new, x_true, f_true, g_true, t_true, Q_flat, c)


    def test_x2z_z2x_c(self):
        xs = [[.6, .1, .3], [.5, .5, .2, .8], [1., .6, .1, .3]]
        zs = [[.6, .7], [.5, .2], [.6, .7]]
        bs = [[0], [0, 2], [0, 1]]
        for x_true, z_true, b in zip(xs, zs, bs):
            x = np.array(x_true)
            z = np.zeros(len(z_true))
            blocks = np.array(b)
            x2z_c(x, z, blocks)
            assert almost_equal(z, z_true)
            x = np.zeros(len(x_true))
            z2x_c(x, z, blocks)
            assert almost_equal(x, x_true)



if __name__ == '__main__':
    unittest.main()