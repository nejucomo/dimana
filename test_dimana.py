#! /usr/bin/env python

import unittest
import dimana


class DimensionalTests (unittest.TestCase):

    def setUp(self):
        self.units = ['m', 'sec', 'kg', 'newton']
        for unit in self.units:
            setattr(self, unit, dimana.Dimensional.get_dimension(unit))

    def test_constants_and_field_identities(self):
        for unitname in self.units:
            unit = getattr(self, unitname)

            self.assertEqual(unit.one, unit.zero + unit.one)
            self.assertEqual(unit.one, unit.one - unit.zero)

            self.assertEqual(unit.zero * unit.zero, unit.zero * unit.one)
            self.assertEqual(dimana.Dimensional.NoDim('0'), unit.zero / unit.one)

    def test_newtons_repr(self):
        conv = self.newton.one / (self.kg.one * self.m.one / (self.sec.one ** 2))

        self.assertEqual('1.0 [(newton*sec^2) / (m*kg)]', repr(conv))





if __name__ == '__main__':
    unittest.main()
