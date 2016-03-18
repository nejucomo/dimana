import unittest
from decimal import Decimal as D
from dimana.units import Units
from dimana.value import Value
from dimana.tests.util import ParseTestClass


class ValueConstructionTests (unittest.TestCase):
    def setUp(self):
        self.meter = Units.parse('meter')

    def test_construction_and_properties(self):
        v = Value(D('42'), self.meter)
        self.assertIs(self.meter, v.units)
        self.assertEqual(D('42'), v.decimal)

    def test_construction_type_error_non_decimal(self):
        self.assertRaises(TypeError, Value, 42, self.meter)

    def test_construction_type_error_non_units(self):
        self.assertRaises(TypeError, Value, 42, 'meter')


class ValueArithmeticTests (unittest.TestCase):
    def test__cmp__(self):
        a = Value.parse('2 [meter / sec]')
        b = Value.parse('2 [meter / sec]')
        c = Value.parse('3 [meter / sec]')

        self.assertEqual(0, cmp(a, b))
        self.assertLess(0, cmp(c, a))
        self.assertGreater(0, cmp(a, c))

    def test__cmp__Mismatch(self):
        a = Value.parse('2 [meter / sec]')
        b = Value.parse('2 [kg]')
        self.assertRaises(Units.Mismatch, cmp, a, b)

    def test__cmp__TypeError(self):
        a = Value.parse('2 [meter / sec]')
        self.assertRaises(TypeError, cmp, a, 'banana')
        self.assertRaises(TypeError, cmp, a, 42)
        self.assertRaises(TypeError, cmp, a, D('42'))

    def test__add__and__sub__ok(self):
        a = Value.parse('2 [meter / sec]')
        b = Value.parse('3 [meter / sec]')
        c = Value.parse('5 [meter / sec]')
        d = Value.parse('-1 [meter / sec]')
        self.assertEqual(c, a+b)
        self.assertEqual(d, a-b)

    def test__add__and__sub__Mismatch(self):
        a = Value.parse('2 [meter / sec]')
        b = Value.parse('3 [kg]')
        self.assertRaises(Units.Mismatch, Value.__add__, a, b)

    def test__mul__and__div__(self):
        a = Value.parse('3 [meter / sec]')
        b = Value.parse('2 [kg]')
        c = Value.parse('6 [kg * meter / sec]')
        d = Value.parse('1.5 [meter / (kg * sec)]')
        self.assertEqual(c, a*b)
        self.assertEqual(d, a/b)

    def test__pow__no_modulus_ok(self):
        a = Value.parse('4 [meter / sec]')
        b = Value.parse('16 [meter^2 / sec^2]')
        self.assertEqual(b, a**2)

    def test__pow__no_modulus_nonint_decimal_power_ok(self):
        a = Value.parse('4 [meter / sec]')
        b = Value.parse('8.0 [meter^1.5 / sec^1.5]')
        self.assertEqual(b, a**D('1.5'))

    def test__pow__TypeError_modulus(self):
        a = Value.parse('3 [meter / sec]')
        self.assertRaises(TypeError, pow, a, 2, 4)

    def test__neg__and__pos__(self):
        a = Value.parse('3 [meter / sec]')
        b = Value.parse('-3 [meter / sec]')
        self.assertIs(a, +a)
        self.assertEqual(b, -a)


@ParseTestClass
class ValueParseAndStringTests (unittest.TestCase):

    targetclass = Value

    def assertParsedValueMatches(self, a, b):
        # Do this to avoid exercising (==) for parser testing. We exercise
        # (==) only in the arithmetic tests for more precise test
        # coverage.
        self.assertEqual(repr(a), repr(b))

    m = Units({'meter': 1})
    s = Units({'sec': 1})
    kg = Units({'kg': 1})

    cases = [
        (Value(D('3.14'), units),
         text,
         alts)
        for (units, text, alts)
        in [
            (Units.scalar,
             '3.14',
             ['3.14 [1]',
              '3.14 [foo^0]',
              '3.14 [x/x]']),

            (s**(-2),
             '3.14 [1 / sec^2]',
             ['3.14 [1/sec^2]',
              '3.14 [sec^-2]',
              '3.14 [1/(sec*sec)]',
              '3.14 [1/ ( sec  * sec )]']),

            (m,
             '3.14 [meter]',
             []),

            (s,
             '3.14 [sec]',
             []),

            (m*s,
             '3.14 [meter * sec]',
             ['3.14 [meter*sec]',
              '3.14 [1/(meter^-1*sec^-1)]']),

            (m/s,
             '3.14 [meter / sec]',
             ['3.14 [sec*meter / sec^2]']),

            (m**2 * s,
             '3.14 [meter^2 * sec]',
             ['3.14 [meter*sec*meter]']),

            (m / s**2,
             '3.14 [meter / sec^2]',
             []),

            (m**2 / s**2,
             '3.14 [meter^2 / sec^2]',
             []),

            (kg**2 * m / s**2,
             '3.14 [kg^2 * meter / sec^2]',
             []),

            (s**2 / (kg*m),
             '3.14 [sec^2 / (kg * meter)]',
             []),
        ]
    ]

    errorcases = [
        # trigger top-level regex:
        '',
        '42 meters',

        # trigger invalid decimal:
        'banana [meter / sec]',

        # trigger Units.ParseError:
        '13 []',
        '1e3 [meter / sec^not-a-number]',
    ]
