#! /usr/bin/env python

import unittest
import dimana


class DimensionalTests (unittest.TestCase):

    def setUp(self):
        self.units = ['m', 'sec', 'kg', 'newton']
        for unit in self.units:
            setattr(self, unit, dimana.Dimensional.get_dimension(unit))

    def test_constants_and_field_identities(self):
        for unit in self.units:
            self.assertEqual(unit.one, unit.zero + unit.one)
            self.assertEqual(unit.one, unit.one - unit.zero)

            self.assertEqual(unit.zero * unit.zero, unit.zero * unit.one)
            self.assertEqual(dimana.Dimensional.NoDim('0'), unit.zero / unit.one)

    def test_newtons_repr(self):
        newtons_per_kilogram_meter_per_second2 = self.newton.one / (self.kg.one * self.m.one / (self.sec ** 2))

        self.assertEqual('1.0 [N * sec^2 / (kg * m)', repr(newtons_per_kilogram_meter_per_second2))



if __name__ == '__main__':
    unittest.main()
