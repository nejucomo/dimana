#! /usr/bin/env python

import unittest
import dimana


class DimensionalTests (unittest.TestCase):

    def setUp(self):
        self.units = []

        for unitname in ['m', 'sec', 'kg', 'newton']:
            unit = dimana.Dimensional.get_dimension(unitname)
            self.units.append(unit)
            setattr(self, unitname, unit)

        # Test dimensionless in all unit-type tests:
        self.units.append(dimana.Dimensional)

    def test_additive_laws(self):
        for u in self.units:
            self.assertEqual(u.one, u.zero + u.one)
            self.assertEqual(u.one, u.one - u.zero)

    def test_multiplicative_laws(self):

        zero = dimana.Dimensional('0')

        for u in self.units:
            self.assertEqual(u.zero * u.zero, u.zero * u.one)
            self.assertEqual(zero, u.zero / u.one)

    def test_power_laws(self):

        one = dimana.Dimensional('1')

        for u in self.units:
            self.assertEqual(one, u.one ** 0)
            self.assertEqual(one, u.zero ** 0)
            self.assertEqual(u.one * u.one, u.one ** 2)
            self.assertEqual(u.inverse.one, u.one ** -1)
            self.assertEqual(one, u.one * (u.one ** -1))

    def test_newtons_repr(self):
        conv = self.newton.one / (self.kg.one * self.m.one / (self.sec.one ** 2))

        self.assertEqual('1.0 [(newton*sec^2) / (m*kg)]', repr(conv))



if __name__ == '__main__':
    unittest.main()
