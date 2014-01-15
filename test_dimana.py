#! /usr/bin/env python

import unittest
import dimana


class DimensionalTests (unittest.TestCase):

    def setUp(self):
        for unit in ['m', 'sec', 'kg', 'newton']:
            setattr(self, unit, dimana.Dimensional.get_dimension(unit))

    def test_newtons_repr(self):
        newtons_per_kilogram_meter_per_second2 = self.newton.one / (self.kg.one * self.m.one / (self.sec ** 2))

        self.assertEqual('1.0 [N * sec^2 / (kg * m)', repr(newtons_per_kilogram_meter_per_second2))



if __name__ == '__main__':
    unittest.main()
