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
             '3.14 [1]',
             ['3.14 [foo^0]',
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
