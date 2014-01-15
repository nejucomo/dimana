#! /usr/bin/env python

import unittest
import dimana


class DimensionalTests (unittest.TestCase):

    def setUp(self):
        self.units = ['m', 'sec', 'kg', 'newton']
        for unit in self.units:
            setattr(self, unit, dimana.Dimensional.get_dimension(unit))

    def test_additive_laws(self):

        @self._test_each_unit
        def add_tests(u):
            self.assertEqual(u.one, u.zero + u.one)
            self.assertEqual(u.one, u.one - u.zero)

    def test_multiplicative_laws(self):

        zero = dimana.Dimensional('0')

        @self._test_each_unit
        def mult_tests(u):
            self.assertEqual(u.zero * u.zero, u.zero * u.one)
            self.assertEqual(zero, u.zero / u.one)

    def test_power_laws(self):

        one = dimana.Dimensional('1')

        @self._test_each_unit
        def mult_tests(u):
            self.assertEqual(one, u.zero ** 0)
            self.assertEqual(one, u.one ** 0)
            self.assertEqual(u.one * u.one, u.one ** 2)
            self.assertEqual(u.inverse.one, u.one ** -1)
            self.assertEqual(one, u.one * (u.one ** -1))

    def test_newtons_repr(self):
        conv = self.newton.one / (self.kg.one * self.m.one / (self.sec.one ** 2))

        self.assertEqual('1.0 [(newton*sec^2) / (m*kg)]', repr(conv))

    def _test_each_unit(self, f):
        for unitname in self.units:
            unit = getattr(self, unitname)
            f(unit)



if __name__ == '__main__':
    unittest.main()
