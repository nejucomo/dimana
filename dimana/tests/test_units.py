#! /usr/bin/env python

import unittest
from dimana.units import Units


class UnitsValueTypeTests (unittest.TestCase):
    def test_value_type_construction(self):
        u1 = Units({})
        u2 = Units({})
        self.assertIs(u1, u2)

        u1 = Units({'meter': 1})
        u2 = Units({'meter': 1})
        self.assertIs(u1, u2)

        u1 = Units({'meter': 1, 'sec': -2})
        u2 = Units({'meter': 1, 'sec': -2})
        self.assertIs(u1, u2)

    def test_scalar(self):
        self.assertIs(Units.scalar, Units({}))


class UnitsArithmeticOperationsTests (unittest.TestCase):
    def setUp(self):
        self.m = Units({'meter': 1})
        self.s = Units({'sec': 1})

        # All equivalences are tested for each case here:
        self.eqcases = [Units.scalar, self.m, self.m * self.s, self.m / self.s]

    def test__mul__(self):
        self.assertIs(
            Units({'meter': 1, 'sec': 1}),
            self.m * self.s,
        )

    def test__mul__TypeError(self):
        self.assertRaises(TypeError, self.m.__mul__, 42)

    def test__div__(self):
        self.assertIs(
            Units({'meter': 1, 'sec': -1}),
            self.m / self.s,
        )

    def test__div__TypeError(self):
        self.assertRaises(TypeError, self.m.__div__, 42)

    def test__pow__(self):
        self.assertIs(
            Units({'meter': 3}),
            self.m ** 3,
        )

    def test__truediv__is__div__(self):
        self.assertEqual(Units.__truediv__, Units.__div__)

    def test_scalar_cancellation_equivalence(self):
        for u in self.eqcases:
            self.assertIs(Units.scalar, u / u)

    def test_scalar_0_power(self):
        for u in self.eqcases:
            self.assertIs(Units.scalar, u ** 0)

    def test_mul_pow_equivalence(self):
        for u in self.eqcases:
            self.assertIs(u * u, u ** 2)

    def test_div_inverse_mul_equivalence(self):
        for u in self.eqcases:
            for k in self.eqcases:
                self.assertIs(u / k, u * (k ** -1))


class UnitsParseAndStrTests (unittest.TestCase):
    def setUp(self):
        self.m = Units({'meter': 1})
        self.s = Units({'sec': 1})

    def test_str_and_repr(self):
        m = self.m
        s = self.s
        kg = Units({'kg': 1})

        cases = [
            ('1', Units.scalar),
            ('1 / sec^2', s**(-2)),
            ('meter', m),
            ('sec', s),
            ('meter * sec', m*s),
            ('meter / sec', m/s),
            ('meter^2 * sec', m**2 * s),
            ('meter / sec^2', m / s**2),
            ('meter^2 / sec^2', m**2 / s**2),
            ('kg^2 * meter / sec^2', kg**2 * m / s**2),
            ('sec^2 / (kg * meter)', s**2 / (kg*m)),
        ]

        for exp, unit in cases:
            self.assertEqual(exp, str(unit))

            repexp = '<Units {}>'.format(exp)
            self.assertEqual(repexp, repr(unit))
