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

    def test__add__(self):
        self.assertIs(self.m, self.m + self.m)

    def test__add__Mismatch(self):
        self.assertRaises(Units.Mismatch, lambda: self.m + self.s)

    def test__add__TypeError(self):
        self.assertRaises(TypeError, lambda: self.m + 'banana')

    def test__inv__(self):
        self.assertIs(self.m, -self.m)

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

    def test__sub__is__add__(self):
        self.assertEqual(Units.__sub__, Units.__add__)

    def test__truediv__is__div__(self):
        self.assertEqual(Units.__truediv__, Units.__div__)

    # Equivalences:
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

    def test_str_repr_and_parse(self):
        m = self.m
        s = self.s
        kg = Units({'kg': 1})

        cases = [
            (Units.scalar,
             '1',
             ['foo^0',
              'x/x']),

            (s**(-2),
             '1 / sec^2',
             ['1/sec^2',
              'sec^-2',
              '1/(sec*sec)',
              '1/ ( sec  * sec )']),

            (m,
             'meter',
             []),

            (s,
             'sec',
             []),

            (m*s,
             'meter * sec',
             ['meter*sec',
              '1/(meter^-1*sec^-1)']),

            (m/s,
             'meter / sec',
             ['sec*meter / sec^2']),

            (m**2 * s,
             'meter^2 * sec',
             ['meter*sec*meter']),

            (m / s**2,
             'meter / sec^2',
             []),

            (m**2 / s**2,
             'meter^2 / sec^2',
             []),

            (kg**2 * m / s**2,
             'kg^2 * meter / sec^2',
             []),

            (s**2 / (kg*m),
             'sec^2 / (kg * meter)',
             []),
        ]

        for unit, text, alts in cases:
            self.assertEqual(text, str(unit))

            repexp = '<Units {!r}>'.format(text)
            self.assertEqual(repexp, repr(unit))

            for t in [text] + alts:
                self.assertIs(unit, Units.parse(t))

    def test_parse_error_empty(self):
        self.assertRaises(Units.ParseError, Units.parse, '')

    def test_parse_error_noise(self):
        self.assertRaises(Units.ParseError, Units.parse, '%^@')

    def test_parse_error_noise_inside_term_pow_parse(self):
        self.assertRaises(Units.ParseError, Units.parse, 'a^*b')

    def test_parse_error_noise_inside_term_uname_parse(self):
        self.assertRaises(Units.ParseError, Units.parse, 'a*^2')

    def test_parse_error_leading_or_trailing_space(self):
        self.assertRaises(Units.ParseError, Units.parse, ' meter')
        self.assertRaises(Units.ParseError, Units.parse, 'meter ')
