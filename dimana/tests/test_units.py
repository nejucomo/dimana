#! /usr/bin/env python

import unittest
from dimana.units import Units


class UnitsTests (unittest.TestCase):
    def test_value_type_construction(self):
        u1 = Units({})
        u2 = Units({})
        self.assertIs(u1, u2)
